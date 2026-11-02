import tkinter as tk
from tkinter import messagebox
import chess
import chess.engine
import shutil
import subprocess
import threading
import random
import os


# ============================================================
# CHESS BOT
# Created by Andreï Barannikov
# ============================================================

WINDOW_TITLE = "Andreï Barannikov's Chess Bot"

BACKGROUND = "#20232B"
BOARD_LIGHT = "#EEEED2"
BOARD_DARK = "#769656"
HIGHLIGHT_COLOR = "#F6F669"
MOVE_DOT_COLOR = "#444444"

WHITE_PIECE_COLOR = "#FFFFFF"
BLACK_PIECE_COLOR = "#111111"

TEXT_COLOR = "#FFFFFF"
ACCENT_COLOR = "#70C1FF"

PIECES = {
    chess.PAWN:   ("♙", "♟"),
    chess.KNIGHT: ("♘", "♞"),
    chess.BISHOP: ("♗", "♝"),
    chess.ROOK:   ("♖", "♜"),
    chess.QUEEN:  ("♕", "♛"),
    chess.KING:   ("♔", "♚"),
}

JOKES = [
    "Interesting move. I will pretend that was part of your plan.",
    "My circuits are confused. And I am the robot.",
    "That move was unexpected. Even for a human.",
    "I have calculated approximately one million possibilities. You chose that one.",
    "Don't worry. I make mistakes too. Just kidding. Usually.",
    "The chessboard is not responsible for your decisions.",
    "I hope you have a plan. I certainly do.",
    "That was a brave move. Possibly too brave.",
    "My evaluation bar just raised an eyebrow.",
    "Are you trying to confuse me? Because it is working. A little.",
    "I have seen better moves in a random number generator.",
    "Your move has been received. My disappointment is processing.",
    "Chess is 99 percent tactics and 1 percent blaming the mouse.",
    "I am not saying that was a blunder. My engine is saying it.",
    "Well, that was certainly one of the moves of all time.",
    "I calculate. Therefore, I am.",
    "You have activated my very expensive silicon brain.",
    "I hope you brought a backup plan.",
    "Let's see what Stockfish thinks about that.",
    "Your king looks nervous. I wonder why.",
    "I was going to make a joke about this position, but it is already a joke.",
    "Excellent. Another opportunity for me to be annoying.",
    "My favorite opening is the one where I win.",
    "You can resign whenever you like. I will not judge you. Much.",
    "I am powered by electricity and questionable humor.",
    "That move deserves a participation trophy.",
    "I would explain my strategy, but I don't want to spoil the surprise.",
    "Your pieces are having a meeting about your decisions.",
    "I am a chess bot, not a miracle worker. Actually, sometimes I am.",
    "The good news is that you still have pieces. The bad news is that I do too.",
]

LEVELS = {
    "Easy": {"depth": 3, "skill": 3},
    "Medium": {"depth": 8, "skill": 10},
    "Strong": {"depth": 14, "skill": 18},
}


class ChessBot:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.configure(bg=BACKGROUND)
        self.root.minsize(650, 650)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        width = min(1050, screen_width - 80)
        height = min(900, screen_height - 100)

        self.root.geometry(f"{width}x{height}")

        self.board = chess.Board()
        self.selected_square = None
        self.legal_targets = []
        self.engine_thinking = False
        self.game_over = False
        self.engine = None
        self.speech_process = None

        self.engine_path = shutil.which("stockfish")

        self.create_interface()
        self.root.bind("<Configure>", self.on_resize)

        if self.engine_path:
            try:
                self.engine = chess.engine.SimpleEngine.popen_uci(
                    self.engine_path
                )
            except Exception as error:
                messagebox.showerror(
                    "Stockfish Error",
                    f"Could not start Stockfish:\n{error}"
                )
                self.engine = None
        else:
            messagebox.showwarning(
                "Stockfish Not Found",
                "Stockfish was not found.\n\n"
                "On a Mac, open Terminal and run:\n"
                "brew install stockfish"
            )

        self.draw_board()
        self.update_status("Your turn! You play White.")
        self.speak("Welcome to Andreï Barannikov's Chess Bot.")

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    # --------------------------------------------------------
    # INTERFACE
    # --------------------------------------------------------

    def create_interface(self):
        self.title_label = tk.Label(
            self.root,
            text="ANDREÏ BARANNIKOV'S CHESS BOT",
            font=("Helvetica", 22, "bold"),
            fg=ACCENT_COLOR,
            bg=BACKGROUND
        )
        self.title_label.pack(pady=(12, 3))

        self.credit_label = tk.Label(
            self.root,
            text="Created by Andreï Barannikov",
            font=("Helvetica", 10, "italic"),
            fg="#BBBBBB",
            bg=BACKGROUND
        )
        self.credit_label.pack(pady=(0, 8))

        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 13, "bold"),
            fg=TEXT_COLOR,
            bg=BACKGROUND
        )
        self.status_label.pack(pady=5)

        self.board_frame = tk.Frame(
            self.root,
            bg=BACKGROUND
        )
        self.board_frame.pack(
            expand=True,
            fill="both",
            padx=15,
            pady=8
        )

        self.canvas = tk.Canvas(
            self.board_frame,
            bg=BACKGROUND,
            highlightthickness=0
        )
        self.canvas.pack(expand=True, fill="both")
        self.canvas.bind("<Button-1>", self.on_board_click)

        controls = tk.Frame(self.root, bg=BACKGROUND)
        controls.pack(pady=(5, 12))

        tk.Label(
            controls,
            text="Difficulty:",
            font=("Helvetica", 11, "bold"),
            fg=TEXT_COLOR,
            bg=BACKGROUND
        ).grid(row=0, column=0, padx=5)

        self.level = tk.StringVar(value="Medium")

        self.level_menu = tk.OptionMenu(
            controls,
            self.level,
            "Easy",
            "Medium",
            "Strong"
        )
        self.level_menu.config(
            font=("Helvetica", 11),
            bg="#383D49",
            fg="white",
            activebackground="#4A5060",
            activeforeground="white",
            highlightthickness=0
        )
        self.level_menu["menu"].config(
            bg="#383D49",
            fg="white"
        )
        self.level_menu.grid(row=0, column=1, padx=5)

        self.new_game_button = tk.Button(
            controls,
            text="New Game",
            command=self.new_game,
            font=("Helvetica", 11, "bold"),
            bg="#3D8B5A",
            fg="white",
            activebackground="#4DAA70",
            activeforeground="white",
            padx=12,
            pady=5
        )
        self.new_game_button.grid(row=0, column=2, padx=5)

        self.undo_button = tk.Button(
            controls,
            text="Undo",
            command=self.undo_move,
            font=("Helvetica", 11, "bold"),
            bg="#4B5368",
            fg="white",
            activebackground="#606A82",
            activeforeground="white",
            padx=12,
            pady=5
        )
        self.undo_button.grid(row=0, column=3, padx=5)

        self.speech_button = tk.Button(
            controls,
            text="Test Voice",
            command=lambda: self.speak(
                "Hello! I am Andreï Barannikov's chess bot."
            ),
            font=("Helvetica", 11, "bold"),
            bg="#315F91",
            fg="white",
            activebackground="#427BB5",
            activeforeground="white",
            padx=12,
            pady=5
        )
        self.speech_button.grid(row=0, column=4, padx=5)

    # --------------------------------------------------------
    # BOARD DRAWING
    # --------------------------------------------------------

    def draw_board(self):
        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 100:
            canvas_width = 650
        if canvas_height < 100:
            canvas_height = 650

        board_size = min(canvas_width, canvas_height)
        square_size = board_size / 8

        left = (canvas_width - board_size) / 2
        top = (canvas_height - board_size) / 2

        self.square_size = square_size
        self.board_left = left
        self.board_top = top

        for row in range(8):
            for col in range(8):
                x1 = left + col * square_size
                y1 = top + row * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size

                square = chess.square(col, 7 - row)

                color = (
                    BOARD_LIGHT
                    if (row + col) % 2 == 0
                    else BOARD_DARK
                )

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=color
                )

                if square == self.selected_square:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=HIGHLIGHT_COLOR,
                        outline=HIGHLIGHT_COLOR
                    )

                # Highlight the last move.
                if self.board.move_stack:
                    last_move = self.board.peek()
                    if square in (
                        last_move.from_square,
                        last_move.to_square
                    ):
                        self.canvas.create_rectangle(
                            x1, y1, x2, y2,
                            fill="#C9D66B",
                            outline="#C9D66B"
                        )

                # Show legal destinations.
                if square in self.legal_targets:
                    cx = (x1 + x2) / 2
                    cy = (y1 + y2) / 2

                    if self.board.piece_at(square):
                        self.canvas.create_oval(
                            x1 + 4, y1 + 4,
                            x2 - 4, y2 - 4,
                            outline=MOVE_DOT_COLOR,
                            width=4
                        )
                    else:
                        radius = square_size * 0.12
                        self.canvas.create_oval(
                            cx - radius, cy - radius,
                            cx + radius, cy + radius,
                            fill=MOVE_DOT_COLOR,
                            outline=MOVE_DOT_COLOR
                        )

                piece = self.board.piece_at(square)

                if piece:
                    self.draw_piece(
                        piece,
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        square_size
                    )

        # File labels.
        for col in range(8):
            x = left + (col + 0.5) * square_size
            y = top + board_size + 2

            if y < canvas_height:
                self.canvas.create_text(
                    x, y,
                    text=chess.FILE_NAMES[col],
                    fill=TEXT_COLOR,
                    font=("Helvetica", 9)
                )

        # Rank labels.
        for row in range(8):
            x = left + 3
            y = top + (row + 0.5) * square_size

            self.canvas.create_text(
                x, y,
                text=str(8 - row),
                fill="#333333",
                font=("Helvetica", 9, "bold")
            )

    def draw_piece(self, piece, x, y, square_size):
        symbol = PIECES[piece.piece_type][0 if piece.color else 1]
        font_size = max(18, int(square_size * 0.70))

        if piece.color == chess.WHITE:
            # White pieces have a solid white fill.
            fill_color = WHITE_PIECE_COLOR
            outline_color = "#222222"
        else:
            fill_color = BLACK_PIECE_COLOR
            outline_color = "#FFFFFF"

        # Draw a solid circular background so the white pieces
        # are not transparent against the chessboard.
        radius = square_size * 0.36

        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill=fill_color,
            outline=outline_color,
            width=max(1, int(square_size * 0.025))
        )

        # Draw the chess symbol on top of the solid background.
        symbol_color = (
            "#111111"
            if piece.color == chess.WHITE
            else "#FFFFFF"
        )

        self.canvas.create_text(
            x,
            y,
            text=symbol,
            font=("DejaVu Sans", font_size),
            fill=symbol_color
        )

    def on_resize(self, event):
        if event.widget == self.root:
            self.draw_board()

    # --------------------------------------------------------
    # MOUSE AND MOVES
    # --------------------------------------------------------

    def on_board_click(self, event):
        if self.engine_thinking or self.game_over:
            return

        if self.board.turn != chess.WHITE:
            return

        col = int(
            (event.x - self.board_left) / self.square_size
        )
        row = int(
            (event.y - self.board_top) / self.square_size
        )

        if not (0 <= row < 8 and 0 <= col < 8):
            return

        square = chess.square(col, 7 - row)
        piece = self.board.piece_at(square)

        if self.selected_square is None:
            if piece and piece.color == chess.WHITE:
                self.selected_square = square
                self.update_legal_targets()
                self.draw_board()
            return

        # Clicking another white piece selects it.
        if piece and piece.color == chess.WHITE:
            self.selected_square = square
            self.update_legal_targets()
            self.draw_board()
            return

        move = chess.Move(self.selected_square, square)

        # Automatically promote to a queen.
        moving_piece = self.board.piece_at(self.selected_square)
        if (
            moving_piece
            and moving_piece.piece_type == chess.PAWN
            and chess.square_rank(square) == 7
        ):
            move.promotion = chess.QUEEN

        if move in self.board.legal_moves:
            self.board.push(move)
            self.selected_square = None
            self.legal_targets = []
            self.draw_board()

            self.check_game_over()

            if not self.game_over:
                self.update_status("Stockfish is thinking...")
                self.root.after(150, self.start_engine_move)
        else:
            self.selected_square = None
            self.legal_targets = []
            self.draw_board()

    def update_legal_targets(self):
        self.legal_targets = []

        if self.selected_square is None:
            return

        for move in self.board.legal_moves:
            if move.from_square == self.selected_square:
                self.legal_targets.append(move.to_square)

    # --------------------------------------------------------
    # STOCKFISH
    # --------------------------------------------------------

    def start_engine_move(self):
        if not self.engine or self.game_over:
            if not self.engine:
                self.update_status(
                    "Stockfish is unavailable. Install it to play."
                )
            return

        if self.board.turn != chess.BLACK:
            return

        settings = LEVELS.get(
            self.level.get(),
            LEVELS["Medium"]
        )

        board_copy = self.board.copy()
        self.engine_thinking = True
        self.set_controls_enabled(False)

        thread = threading.Thread(
            target=self.engine_move_worker,
            args=(board_copy, settings),
            daemon=True
        )
        thread.start()

    def engine_move_worker(self, board_copy, settings):
        move = None
        error_message = None

        try:
            self.engine.configure({
                "Skill Level": settings["skill"]
            })

            result = self.engine.play(
                board_copy,
                chess.engine.Limit(depth=settings["depth"])
            )
            move = result.move

        except Exception as error:
            error_message = str(error)

        self.root.after(
            0,
            lambda: self.finish_engine_move(move, error_message)
        )

    def finish_engine_move(self, move, error_message):
        self.engine_thinking = False
        self.set_controls_enabled(True)

        if error_message:
            self.update_status("Stockfish encountered an error.")
            print("Stockfish error:", error_message)
            return

        if move is None or self.game_over:
            return

        if move not in self.board.legal_moves:
            return

        self.board.push(move)
        self.draw_board()
        self.check_game_over()

        if not self.game_over:
            self.update_status("Your turn! Good luck.")
            self.speak(random.choice(JOKES))

    def set_controls_enabled(self, enabled):
        state = "normal" if enabled else "disabled"

        self.new_game_button.config(state=state)
        self.undo_button.config(state=state)
        self.level_menu.config(state=state)
        self.speech_button.config(state=state)

    # --------------------------------------------------------
    # GAME MANAGEMENT
    # --------------------------------------------------------

    def new_game(self):
        if self.engine_thinking:
            return

        self.board.reset()
        self.selected_square = None
        self.legal_targets = []
        self.game_over = False

        self.draw_board()
        self.update_status("New game! You play White.")
        self.speak("A new game. Let's make some questionable decisions.")

    def undo_move(self):
        if self.engine_thinking:
            return

        if not self.board.move_stack:
            return

        # Undo the engine move and then the player's move if present.
        self.board.pop()

        if self.board.move_stack and self.board.turn == chess.BLACK:
            self.board.pop()

        self.selected_square = None
        self.legal_targets = []
        self.game_over = False

        self.draw_board()
        self.update_status("Move undone. Try a different idea.")

    def check_game_over(self):
        if not self.board.is_game_over():
            return

        self.game_over = True

        if self.board.is_checkmate():
            if self.board.turn == chess.WHITE:
                message = "Checkmate! Stockfish wins."
                spoken = "Checkmate! I win. I would say good game, but I am a robot."
            else:
                message = "Checkmate! You win!"
                spoken = "You won! Incredible. I shall investigate this suspicious event."
        elif self.board.is_stalemate():
            message = "Draw by stalemate."
            spoken = "A stalemate. Nobody wins. My favorite kind of paperwork."
        elif self.board.is_insufficient_material():
            message = "Draw: insufficient material."
            spoken = "Draw. There are not enough pieces left to cause trouble."
        elif self.board.is_seventyfive_moves():
            message = "Draw by the seventy-five-move rule."
            spoken = "Draw by the seventy-five-move rule. That was a lot of moving."
        elif self.board.is_fivefold_repetition():
            message = "Draw by repetition."
            spoken = "Draw by repetition. We have officially gone in circles."
        else:
            message = "Game over: draw."
            spoken = "The game is over. A draw. Well played."

        self.update_status(message)
        self.speak(spoken)

        messagebox.showinfo("Game Over", message)

    # --------------------------------------------------------
    # VOICE
    # --------------------------------------------------------

    def speak(self, text):
        # macOS built-in speech. The GUI remains responsive.
        if os.name != "posix":
            return

        if self.speech_process and self.speech_process.poll() is None:
            try:
                self.speech_process.terminate()
            except Exception:
                pass

        try:
            self.speech_process = subprocess.Popen(
                ["say", "-v", "Samantha", text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass

    def update_status(self, text):
        self.status_label.config(text=text)

    def close_app(self):
        if self.speech_process and self.speech_process.poll() is None:
            try:
                self.speech_process.terminate()
            except Exception:
                pass

        if self.engine:
            try:
                self.engine.quit()
            except Exception:
                pass

        self.root.destroy()


# ============================================================
# START THE BOT
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessBot(root)
    root.mainloop()
