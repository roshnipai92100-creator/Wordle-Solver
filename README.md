# Wordle Solver

A Python-based Wordle solver that filters possible answers using Wordle feedback and recommends guesses through a letter-frequency scoring algorithm.

The project focuses on exploring different word-selection strategies and measuring their performance through automated benchmarking.

## Disclaimer
All versions of Wordle may not work. This solver is general and includes the original 2,315 possible answers and 12,972 valid guesses. 

## Features

- Filters possible answers based on previous guesses and feedback.
- Supports Wordle's green, yellow, and gray feedback system.
- Handles repeated letters when generating feedback.
- Validates user guesses and feedback.
- Recommends the next guess using letter-frequency scoring.
- Displays the number of remaining possible answers.
- Includes automated benchmarking against all 2,315 possible answers.

## How It Works

The solver begins with a list of possible Wordle answers.

After each guess, the user enters the corresponding feedback:

| Symbol | Meaning |
|---|---|
| G | Green — correct letter in the correct position |
| Y | Yellow — correct letter in the wrong position |
| X | Gray — letter is not present, or all available occurrences have already been accounted for |

The solver compares the feedback against every remaining possible answer and eliminates words that are inconsistent with the results.

It then recommends a new guess based on the remaining candidates.

### Guess Suggestion Algorithm (v1.1.0)

The current algorithm uses letter-frequency scoring.

1. Count how many remaining answers contain each unique letter.
2. Calculate a score for each remaining answer by adding the frequencies of its unique letters.
3. Recommend the word with the highest score.

Repeated letters are counted only once during scoring to avoid unnecessarily rewarding duplicate letters.

The algorithm prioritizes commonly occurring letters to help narrow down the remaining possibilities.

## Installation

### Requirements

- Python 3
- No external Python packages required

Clone the repository:

```bash
git clone https://github.com/roshnipai92100-creator/wordle-solver.git
```

Navigate into the project directory:

```bash
cd wordle-solver
```

Run the solver:

```bash
python main.py
```

Make sure `answers.txt` and `guesses.txt` are present in the project directory.

## Usage

1. Enter a valid five-letter Wordle guess.
2. Enter the feedback received from Wordle using X, Y, and G.
3. Review the remaining possible answers and the suggested next guess.
4. Repeat until the answer is found or six guesses have been used.

Example:

```text
Guess: crane
Feedback (X = Gray, Y = Yellow, G = Green): XXYXG

Suggested next guess: ...
Guess score: ...
```

The suggestion and score depend on the current list of remaining answers.

## Benchmarks

The solver is evaluated by simulating games against all 2,315 possible answers.

| Metric | v1.0.0 | v1.1.0 |
|---|---:|---:|
| Algorithm | Random selection | Letter-frequency scoring |
| Solve rate | 98.28% | 99.05% |
| Average guesses (wins) | 4.029 | 3.650 |
| Average execution time | 3.818 ms | 7.494 ms |
| Filtering accuracy (self-consistency) | 100% | 100% |

The v1.0.0 results represent averages across 30 random seeds. The v1.1.0 results come from one deterministic benchmark covering all possible answers.

**v1.1.0 reduced the average number of guesses for successful games by approximately 9.4%.**

Run the current benchmark with:

```bash
python benchmark.py
```

For detailed results and testing methodology, see [BENCHMARK.md](BENCHMARK.md).

## Version History

### v1.1.0 — Letter Frequency Scoring
- Introduced automated guess suggestions.
- Added frequency-based candidate scoring.
- Improved solve rate and average guess efficiency.

### v1.0.0 — Initial Release
- Implemented Wordle feedback processing.
- Added answer filtering.
- Established automated benchmarking with random guess selection.

## Planned Improvements

- Position-based letter-frequency scoring.
- More advanced guess-selection strategies.
- Evaluation of guesses outside the remaining answer list.
- Additional benchmark comparisons.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE.md) for details.
