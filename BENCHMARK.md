# Wordle Solver Benchmarks

This document tracks the performance of each Wordle Solver version as new guess-selection algorithms are implemented.

## Testing Methodology

Each benchmark simulates games using every word in `answers.txt` as the secret answer.

- Possible answers: 2,315
- Maximum guesses per game: 6
- Successful game: The correct answer is found within six guesses.
- Failed game: The correct answer is not found within six guesses.
- Worst-case score: 7 represents a failed game, not an actual seventh guess.
- Average guesses: Calculated using successful games only.
- Execution time: Average simulation time per game, excluding human input.

The filtering accuracy metric checks whether the actual answer remains in the candidate list after filtering. Since the benchmark uses the same feedback function to generate and evaluate feedback, independent tests are required to validate Wordle feedback correctness.

---

## v1.0.0 — Random Guessing Baseline

### Algorithm

Randomly selects a word from the remaining possible answers.

### Testing Configuration

- Random seeds: 30 (0–29)
- Games per seed: 2,315
- Total simulated games: 69,450

### Results

| Metric | Result |
|---|---:|
| Mean solve rate | 98.28% |
| Mean average guesses | 4.029 |
| Mean execution time | 3.818 ms |
| Filtering accuracy (self-consistency) | 100% |
| Best seed solve rate | 99.18% |
| Worst seed solve rate | 97.54% |
| Total failed games | 1,198 |

---

## v1.1.0 — Letter Frequency Scoring

### Algorithm

Counts how many remaining possible answers contain each unique letter.

Each candidate word receives a score equal to the sum of its unique letters' frequencies. The highest-scoring remaining answer is selected as the recommended guess.

Repeated letters are counted only once per word during scoring.

### Testing Configuration

- Algorithm: Deterministic
- Test run: Seed 0 (seed does not affect guess selection)
- Total simulated games: 2,315

### Results

| Metric | Result |
|---|---:|
| Successful games | 2,293 |
| Failed games | 22 |
| Solve rate | 99.05% |
| Average guesses (wins) | 3.650 |
| Worst-case score | 7 (failure sentinel) |
| Average execution time | 7.494 ms |
| Filtering accuracy (self-consistency) | 100% |

### Average Remaining Candidates

These values represent the average number of candidates after each unsuccessful guess, among games that reached that stage.

| Guess | Average remaining candidates |
|---|---:|
| 1 | 71.63 |
| 2 | 5.12 |
| 3 | 1.89 |
| 4 | 1.70 |
| 5 | 1.75 |

Later-turn averages may increase because they are calculated over different subsets of games.

---

## Version Comparison

| Metric | v1.0.0 | v1.1.0 | Change |
|---|---:|---:|---:|
| Solve rate | 98.28% | 99.05% | +0.77 pp |
| Average guesses | 4.029 | 3.650 | -9.4% |
| Average game time | 3.818 ms | 7.494 ms | +96.3% |
| Filtering accuracy (self-consistency) | 100% | 100% | No change |

### Conclusion

Letter-frequency scoring improves guess efficiency compared with random remaining-answer selection.

The v1.1.0 algorithm achieves a higher solve rate and requires approximately 9.4% fewer guesses on average for successful games.

However, it also introduces additional computational overhead, nearly doubling average execution time.

Future benchmarks will evaluate whether position-based scoring and other information-based strategies can improve solve rate and guess efficiency further.

# Wordle Solver Benchmarks

## v1.0.0 — Random Guessing Baseline

**Algorithm:** Randomly selects a word from the remaining possible answers.

### Testing Methodology
- Possible answers: 2,315
- Random seeds: 30 (0–29)
- Total simulated games: 69,450
- Maximum guesses per game: 6
- Every possible answer is tested once per seed.

### Results

| Metric | Result |
|---|---:|
| Mean solve rate | 98.28% |
| Total successful games | 68,252 |
| Total failed games | 1,198 |
| Average guesses (successful games) | 4.029 |
| Average execution time per game | 3.818 ms |
| Reported filtering accuracy | 100% |
| Best seed solve rate | 99.18% |
| Worst seed solve rate | 97.54% |

### Next Version Goals (v1.1.0)
- Implement letter-frequency-based guess scoring.
- Achieve a solve rate above 99%.
- Reduce average guesses below 4.000.
- Compare results against the random baseline using identical test conditions.

**Note:** Filtering accuracy is measured using the same feedback function as the simulation. Independent feedback tests are also necessary.
