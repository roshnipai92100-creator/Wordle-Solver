# Create Possible Answers and Possible Guesses Lists

with open("answers.txt", "r") as file:
    possible_answers = file.read().splitlines()

with open("guesses.txt", "r") as file:
    possible_guesses = set(file.read().splitlines() + possible_answers)

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

# Run Guess + Answers -> Filter 6 Times
for i in range(6):
    # Get Guess + Feedback From User
    while True:
        guess = str(input("Guess: ")).lower()
        if guess in possible_guesses:
            break
        else:
            print("Invalid input")
    while True:
        feedback = str(input("Feedback (X = Gray, Y = Yellow, G = Green): ")).upper()
        if len(feedback) == 5 and all(letter in "XYG" for letter in feedback):
            guess_history.append((guess, feedback))
            break
        else:
            print("Invalid input")

    # Check if set(feedback) == {'G'} (feedback only contains G's)
    if set(feedback) == {'G'}:
        print("Correct Answer Found!")
        break

    # Filter Out Non-Matching Answers
    remaining_answers = [answer for answer in remaining_answers if get_feedback(guess, answer) == feedback]
    print(f"{len(remaining_answers)} answers remaining")
    print(f"Remaining answers: {remaining_answers}")

# All 6 guesses are used and correct answer not found
if set(feedback) != {'G'}:
    print("No more guesses")