# Andreï Barannikov's Chess Bot

A chess bot that I create using Stockfish.

## Requirements

Before running the bot, make sure you have:

- Python 3.10 or newer
- pip
- Stockfish
- macOS for the built-in voice commentary

The chess game itself uses Python and Stockfish. The voice feature uses the macOS `say` command.

## Installation

### 1. Install Python

Download Python from the official website:

https://www.python.org/downloads/

### 2. Install Stockfish

Stockfish is the chess engine that powers the bot.

On macOS, open Terminal and run:

```bash
brew install stockfish
```

### 3. Download the project

Clone this repository:

```bash
git clone https://github.com/barannikovandrei/chessbot.git
```

Alternatively, click **Code → Download ZIP** on GitHub and extract the downloaded folder.

### 4. Open the project folder

In Terminal, navigate to the folder containing `chess_bot.py`.

For example:

```bash
cd chess-bot
```

Replace `chess-bot` with your actual folder name.

### 5. Install the Python dependency

Run:

```bash
python3 -m pip install python-chess
```

### 6. Launch the bot

Run:

```bash
python3 chess_bot.py
```

The chess window should open, allowing you to start playing!

## 🎮 How to Play

1. Launch the program.
2. Select a difficulty level: **Easy**, **Medium**, or **Strong**.
3. Play as White. Stockfish plays as Black.
4. Click a piece to select it.
5. Click a square to move the piece.
6. Use **Undo** to take back moves.
7. Use **New Game** to start a fresh match.
8. Click **Test Voice** to test the voice commentary.

Actual playing strength depends on the Stockfish version and the computer running it.

## Voice Commentary

The bot can speak its comments aloud using macOS text-to-speech.

The current version uses the `Samantha` English voice.

If the voice does not work, open Terminal and test:

```bash
say -v Samantha "Hello! I am Andreï Barannikov's Chess Bot."
```

To see which voices are available on your Mac, run:

```bash
say -v '?'
```

If Samantha is unavailable, change `"Samantha"` in `chess_bot.py` to an English voice installed on your computer.

**Note:** Voice commentary currently relies on macOS and is not configured for Windows or Linux.


## ❓ Troubleshooting

### Stockfish was not found

Make sure Stockfish is installed:

```bash
brew install stockfish
```

Then check whether your terminal can find it:

```bash
which stockfish
```

If Stockfish is installed but the program still cannot find it, you may need to configure the Stockfish executable path in the Python code.

### Python cannot find the chess module

Install the required dependency:

```bash
python3 -m pip install python-chess
```

### The voice does not work

Make sure you are running macOS and test the `say` command in Terminal.

Check that the voice configured in the Python code is installed.

### The chess window does not open

Check that Python is installed correctly and that Tkinter is available in your Python installation.

## 👨‍💻 Author

**Andreï Barannikov**

Using Stockfish (I do not wish to train my own chess model)
---

**Enjoy the game, improve your chess, and try not to make Stockfish laugh!** 
