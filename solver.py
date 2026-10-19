from pathlib import Path

# Create Possible Answers and Possible Guesses Lists
FOLDER = Path(__file__).resolve().parent

with open(FOLDER / "answers.txt", "r") as file:
    possible_answers = file.read().splitlines()

with open(FOLDER / "guesses.txt", "r") as file:
    possible_guesses = set(file.read().splitlines() + possible_answers)

# Create answer_found Boolean

answer_found = False

# Create Remaining Answers and Guess History Lists

remaining_answers = possible_answers.copy()

guess_history = []

# Create Guess Scores Dictionary ("Word": Score)

guess_scores = {}

# get_feedback(): Compare Hypothetical Answer Feedback to Guess Feedback to Remove Non-Matching Answers

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

def solve_history(history):
    remaining = possible_answers.copy()

    for guess, feedback in history:

        guess = guess.lower()
        feedback = feedback.upper()

        if guess not in possible_guesses:
            raise ValueError(f"Invalid guess: {guess}")

        if len(feedback) != 5 or any(
            letter not in "XYG" for letter in feedback
        ):
            raise ValueError(f"Invalid feedback: {feedback}")

        remaining = [
            answer
            for answer in remaining
            if get_feedback(guess, answer) == feedback
        ]

        if not remaining:
            return {
                "remaining": [],
                "suggestion": None,
                "score": None,
                "solved": False
            }

    # No guesses have been submitted yet.
    if not history:
        return {
            "remaining": remaining,
            "suggestion": "alert",
            "score": None,
            "solved": False
        }

    # The most recent guess was completely correct.
    if history[-1][1].upper() == "GGGGG":
        return {
            "remaining": remaining,
            "suggestion": None,
            "score": None,
            "solved": True
        }

    # Only one possible answer remains.
    if len(remaining) == 1:
        return {
            "remaining": remaining,
            "suggestion": remaining[0],
            "score": None,
            "solved": False
        }

    best_guess, score = suggest_guess(remaining)

    return {
        "remaining": remaining,
        "suggestion": best_guess,
        "score": score,
        "solved": False
    }

def main():
    global answer_found, remaining_answers

    print(f"Suggested next guess: ALERT")
    print(f"Guess score: 4117\n")

    # Run Until Answer is Found
    while not answer_found:
        # Get Guess + Feedback From User
        while True:
            guess = str(input("Guess: ")).lower()
            if guess in possible_guesses:
                break
            else:
                print("Invalid input")
        while True:
            feedback = str(input("Feedback (X = Gray, Y = Yellow, G = Green): ")).upper()
            if len(feedback) == 5 and not all([feedback.count('G') == 4, feedback.count('Y') == 1]) and all(letter in "XYG" for letter in feedback):
                guess_history.append((guess, feedback))
                break
            else:
                print("Invalid input")

        # Check if set(feedback) == {'G'} (feedback only contains G's)
        if set(feedback) == {'G'}:
            print("Answer Found!")
            answer_found = True
            break

        # Filter Out Non-Matching Answers
        remaining_answers = [answer for answer in remaining_answers if get_feedback(guess, answer) == feedback]
        if remaining_answers:
            if len(remaining_answers) > 1:
                print(f"\n{len(remaining_answers)} answers remaining")
                print(f"Remaining answers: {remaining_answers}\n")

                best_guess, score = suggest_guess(remaining_answers)

                print(f"Suggested next guess: {best_guess.upper()}")
                print(f"Guess score: {score}\n")

            else:
                print(f"Answer: {remaining_answers[0].upper()}")
                answer_found = True

        else:
            print("No possible answers remain. Check your feedback.")

if __name__ == "__main__":
    main()