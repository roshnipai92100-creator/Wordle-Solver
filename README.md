# Wordle Solver

A Python Wordle solver with automatic screen reading, OCR, and a desktop interface.

The project combines a feedback-based word filtering algorithm with OpenCV, Tesseract OCR, and Tkinter to read a Wordle board directly from the screen and recommend the next guess.

## Features

### Solving Algorithm
- Filters possible answers using Wordle's feedback rules.
- Correctly handles repeated letters.
- Scores remaining answers using letter frequency.
- Recommends the highest-scoring remaining answer.
- Supports multiple guesses and their corresponding feedback.
- Includes a terminal interface for manual play.

### Automatic Screen Reader
- Captures the Wordle board directly from the screen.
- Detects and organizes all 30 tiles using OpenCV.
- Removes duplicate tile detections.
- Identifies green, yellow, gray, and empty tiles.
- Supports light, dark, and high-contrast Wordle themes.
- Uses Tesseract OCR to recognize letters in completed rows.
- Converts visual feedback into a format understood by the solver.

### Desktop GUI
- Built with Tkinter.
- Displays a visual representation of the detected board.
- Supports window resizing.
- Includes an optional Always on Top setting.
- Automatically minimizes during screen capture.
- Displays the recommended next guess and remaining candidate count.
- Rejects incomplete or uncertain OCR results rather than silently passing them to the solver.

## How It Works

1. Open Wordle in your browser.
2. Launch the desktop application.
3. Enter and submit a guess in Wordle.
4. Click **Scan Wordle** in the application.
5. The program captures the screen and identifies the board.
6. OpenCV detects tile positions and feedback colors.
7. Tesseract reads the letters.
8. The detected guess history is passed to the solver.
9. The application displays the recommended next guess.

The application reads the board and provides recommendations. It does not automatically type or submit guesses.

## Installation

### Requirements

- Python
- Tesseract OCR
- A graphical desktop environment
- The dependencies listed below

Install the Python packages:

```bash
pip install numpy opencv-python pyautogui pytesseract pillow
```

Tkinter is included with most standard Python installations.

Install Tesseract OCR separately and configure its executable location in `config.py`:

```python
TESSERACT_PATH = r"C:\path\to\tesseract.exe"
```

Update the path to match your installation.

### Word Lists

Place the following files in the same directory as `solver.py`:

- `answers.txt` — possible Wordle answers.
- `guesses.txt` — additional valid guesses.

## Usage

Launch the graphical application:

```bash
python gui.py
```

Alternatively, launch the original terminal-based solver:

```bash
python solver.py
```

The GUI captures the visible screen, so make sure the Wordle board is fully visible and its animations have finished before scanning.

## Project Structure

```text
Wordle-Solver/
├── gui.py
├── main.py
├── solver.py
├── screen_reader.py
├── board_detector.py
├── tile_reader.py
├── config.py
├── answers.txt
├── guesses.txt
└── README.md
```

| File | Purpose |
|---|---|
| `gui.py` | Desktop application |
| `main.py` | Screen-reading test entry point |
| `solver.py` | Filtering and recommendation algorithm |
| `screen_reader.py` | Screenshot capture |
| `board_detector.py` | Tile detection and grid organization |
| `tile_reader.py` | Color recognition and OCR |
| `config.py` | Shared settings and reference colors |

## Solver Algorithm

The solver begins with a list of possible answers.

For every submitted guess, it compares the actual feedback against the feedback that would be produced by each hypothetical answer.

Candidates producing different feedback are eliminated.

For the remaining candidates, the solver calculates letter frequencies and scores each possible answer based on its unique letters. The highest-scoring remaining answer is recommended.

This approach keeps the solving algorithm independent of the screen-reading and GUI components.

## Limitations

- Screen detection depends on the Wordle board being visible.
- OCR can occasionally misidentify individual letters.
- Screenshots taken during tile animations may produce incorrect feedback.
- Changes to Wordle's visual design may require adjustments to detection settings.
- The application currently requires a locally installed Tesseract executable.

## Benchmarking

Algorithm performance and application performance are measured separately.

Algorithm benchmarks evaluate solve rate, average guesses, filtering accuracy, and execution time.

Application benchmarks evaluate screenshot capture, board detection, color recognition, OCR accuracy, and total Scan & Solve time.

Adding a graphical interface does not change the underlying solving algorithm, but screen capture and OCR introduce additional processing time.

## License

See the `LICENSE` file for licensing information.

## Disclaimer

This is an independent educational project and is not affiliated with or endorsed by The New York Times or Wordle.
