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
