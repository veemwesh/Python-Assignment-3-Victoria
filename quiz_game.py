"""
Quiz Game
A Python trivia quiz game with score tracking and a leaderboard.
Questions are loaded from questions.csv (a real dataset), 5 chosen at
random per round.
Built to practice core data types: str, int, float, bool, list, dict,
tuple, set.
"""

import random
import csv


def load_questions(filename="questions.csv"):
    """Read questions from a CSV file and build the list of dicts."""
    loaded = []
    with open(filename, "r", newline="") as f:
        # reads each row as a dict, using the header row as keys
        reader = csv.DictReader(f)
        for row in reader:
            question_dict = {
                "question": row["question"],
                "options": [
                    row["option1"],
                    row["option2"],
                    row["option3"],
                    row["option4"],
                ],
                "answer": row["answer"],
                "category": row["category"],
            }
            loaded.append(question_dict)
    return loaded


questions = load_questions()   # list of dicts, loaded from questions.csv

leaderboard = []          # list of tuples: (player_name, score, percentage)
categories_played = set()  # set: unique categories seen this session


def play_quiz():
    name = input("Enter your name: ")   # str
    print(
        f"\nHi {name}! Answer each question by typing the option text "
        "exactly.\n"
    )

    score = 0  # int

    quiz_questions = random.sample(questions, k=min(5, len(questions)))

    for q in quiz_questions:
        print(q["question"])
        for i, option in enumerate(q["options"], start=1):
            print(f"  {i}. {option}")

        answer = input("Your answer: ").strip()  # str

        is_correct = answer.lower() == q["answer"].lower()  # bool
        if is_correct:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong. The correct answer was: {q['answer']}\n")

        categories_played.add(q["category"])  # avoids duplicates

    total = len(quiz_questions)               # int
    percentage = (score / total) * 100        # float

    print(f"Quiz finished, {name}!")
    print(f"Score: {score}/{total}")
    print(f"Percentage: {percentage:.1f}%")
    print(f"Type of percentage: {type(percentage)}\n")

    # --- tuple: an immutable record for the leaderboard ---
    entry = (name, score, percentage)
    leaderboard.append(entry)
    print(f"Leaderboard entry created: {entry} (type: {type(entry)})\n")


def show_leaderboard():
    if not leaderboard:
        print("No scores yet. Play a quiz first!\n")
        return

    # sort by score, highest first
    sorted_board = sorted(
        leaderboard, key=lambda entry: entry[1], reverse=True
    )

    print("---- Leaderboard ----")
    for i, (name, score, percentage) in enumerate(sorted_board, start=1):
        print(f"{i}. {name} - {score} pts ({percentage:.1f}%)")
    print()


def show_categories():
    if not categories_played:
        print("No categories played yet.\n")
        return
    print(f"Categories covered this session: {categories_played}")
    print(f"Type: {type(categories_played)}")
    print(f"Number of unique categories: {len(categories_played)}\n")


def save_leaderboard(filename="leaderboard.txt"):
    with open(filename, "w") as f:
        for name, score, percentage in leaderboard:
            f.write(f"{name},{score},{percentage}\n")
    print(f"Saved {len(leaderboard)} score(s) to {filename}.\n")


def load_leaderboard(filename="leaderboard.txt"):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"No file called {filename} found yet.\n")
        return

    leaderboard.clear()
    for line in lines:
        parts = line.strip().split(",")   # everything here is still a str!
        name = parts[0]                          # stays a str
        score = int(parts[1])                     # str -> int
        percentage = float(parts[2])               # str -> float
        leaderboard.append((name, score, percentage))

    print(f"Loaded {len(leaderboard)} score(s) from {filename}.\n")


def main():
    while True:
        print("---- Quiz Game ----")
        print("1. Play quiz")
        print("2. Show leaderboard")
        print("3. Show categories played")
        print("4. Save leaderboard to file")
        print("5. Load leaderboard from file")
        print("6. Quit")
        choice = input("Choose an option (1-6): ")

        if choice == "1":
            play_quiz()
        elif choice == "2":
            show_leaderboard()
        elif choice == "3":
            show_categories()
        elif choice == "4":
            save_leaderboard()
        elif choice == "5":
            load_leaderboard()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.\n")


if __name__ == "__main__":
    main()
