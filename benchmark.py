import random
import time
from statistics import mean

# Load the same answer list used by main.py
with open("answers.txt", "r") as file:
    possible_answers = file.read().splitlines()


# Restate get_feedback function
def get_feedback(guess, answer):
    result = ["X"] * 5
    remaining = list(answer)

    # First, find green letters
    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = 'G'
            remaining[i] = None

    # Next, find yellow letters
    for i in range(5):
        if result[i] != 'G' and guess[i] in remaining:
            result[i] = 'Y'
            remaining[remaining.index(guess[i])] = None

    return ''.join(result)

def suggest_guess(remaining_answers):
    letter_frequency = {}

    # Count how many answers contain each letter
    for answer in remaining_answers:
        for letter in set(answer):
            letter_frequency[letter] = letter_frequency.get(letter, 0) + 1

    # Score each remaining answer
    guess_scores = {}

    for guess in remaining_answers:
        score = 0

        for letter in set(guess):
            score += letter_frequency[letter]

        guess_scores[guess] = score

    best_guess = max(guess_scores, key=guess_scores.get)

    return best_guess, guess_scores[best_guess]

# Simulate one complete Wordle game
def simulate_game(secret_answer, rng):
    remaining_answers = possible_answers.copy()

    candidate_counts = []
    filtering_correct = True

    start = time.perf_counter()

    for turn in range(1, 7):

        # Pick a random word from the remaining candidates
        if not remaining_answers:
            break

        guess, score = suggest_guess(remaining_answers)

        # Generate the feedback automatically
        feedback = get_feedback(guess, secret_answer)

        # Check whether the solver won
        if feedback == "GGGGG":
            elapsed = time.perf_counter() - start

            return {
                "solved": True,
                "guesses": turn,
                "filtering_correct": filtering_correct,
                "candidate_counts": candidate_counts,
                "time": elapsed
            }

        # Apply your existing filtering algorithm
        remaining_answers = [
            answer
            for answer in remaining_answers
            if get_feedback(guess, answer) == feedback
        ]

        candidate_counts.append(len(remaining_answers))

        # The actual answer should NEVER be eliminated
        if secret_answer not in remaining_answers:
            filtering_correct = False

    elapsed = time.perf_counter() - start

    return {
        "solved": False,
        "guesses": 7,
        "filtering_correct": filtering_correct,
        "candidate_counts": candidate_counts,
        "time": elapsed
    }


# Run the benchmark against every possible answer
def run_benchmark(seed=42):
    rng = random.Random(seed)

    results = []

    for answer in possible_answers:
        result = simulate_game(answer, rng)
        results.append(result)

    total_games = len(results)

    wins = [r for r in results if r["solved"]]
    losses = [r for r in results if not r["solved"]]

    correct_filters = sum(
        r["filtering_correct"] for r in results
    )

    solve_rate = len(wins) / total_games * 100
    filtering_accuracy = correct_filters / total_games * 100

    average_guesses = (
        mean(r["guesses"] for r in wins)
        if wins else 0
    )

    worst_case = max(r["guesses"] for r in results)

    average_time = mean(r["time"] for r in results)

    # Calculate average candidates remaining after each turn
    average_candidates = []

    for turn in range(5):
        counts = [
            r["candidate_counts"][turn]
            for r in results
            if len(r["candidate_counts"]) > turn
        ]

        average_candidates.append(
            mean(counts) if counts else None
        )

    print(f"\nWORDLE BENCHMARK — SEED {seed}")
    print("-" * 40)

    print(f"Total games:       {total_games}")
    print(f"Successful games:  {len(wins)}")
    print(f"Failed games:      {len(losses)}")

    print(f"Filtering accuracy: {filtering_accuracy:.2f}%")
    print(f"Solve rate:         {solve_rate:.2f}%")
    print(f"Average guesses:    {average_guesses:.3f}")
    print(f"Worst-case guesses: {worst_case}")
    print(f"Average game time:  {average_time * 1000:.3f} ms")

    print("\nAVERAGE REMAINING CANDIDATES")

    for turn, count in enumerate(average_candidates, start=1):
        if count is not None:
            print(f"After guess {turn}: {count:.2f}")

    return {
        "solve_rate": solve_rate,
        "average_guesses": average_guesses,
        "worst_case": worst_case,
        "average_time": average_time,
        "filtering_accuracy": filtering_accuracy
    }


# Run the benchmark
if __name__ == "__main__":
    run_benchmark(0)