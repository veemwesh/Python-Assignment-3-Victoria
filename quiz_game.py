"""
Quiz Game
A Python trivia quiz game with score tracking and a leaderboard.
Questions are loaded from questions.csv (a real dataset). Five are chosen
at random per round.
Also includes an online module: option 6 calls the Groq API to generate
a live AI question, so the game works both offline (CSV) and online (Groq).
Built to practice core data types: str, int, float, bool, list,
    dict, tuple, set.
"""

import random
import csv
import os
import json
import requests


def load_questions(filename="questions.csv"):
    """Read questions from a CSV file and build the list of dicts."""
    loaded = []
    with open(filename, "r", newline="") as f:
        reader = csv.DictReader(f)   # reads each row as a dict, using the header row as keys
        for row in reader:
            question_dict = {
                "question": row["question"],
                "options": [row["option1"], row["option2"], row["option3"], row["option4"]],
                "answer": row["answer"],
                "category": row["category"],
            }
            loaded.append(question_dict)
    return loaded


questions = load_questions()   # list of dicts, loaded from questions.csv

leaderboard = []          # list of tuples: (player_name, score, percentage)
categories_played = set()  # set: unique categories seen this session

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"


def get_groq_api_key():
    """Look for the key as an environment variable first, otherwise ask for it."""
    key = os.getenv("GROQ_API_KEY")   # str, or None if not set
    if not key:
        key = input("Enter your Groq API key: ").strip()
    return key


def ask_groq_for_question():
    """
    Calls the Groq API and asks it to generate one trivia question.
    Returns a dict shaped exactly like the questions loaded from the CSV,
    so it can be reused with the same answering logic.
    """
    api_key = get_groq_api_key()

    prompt = (
        "Generate one original multiple-choice trivia question. "
        "Reply with ONLY valid JSON, no extra text, in exactly this shape: "
        '{"question": "...", "options": ["...", "...", "...", "..."], '
        '"answer": "...", "category": "..."}. '
        "The answer must match one of the options exactly."
    )

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=15)
    response.raise_for_status()   # raises an error if Groq rejected the request
    result = response.json()

    content = result["choices"][0]["message"]["content"]   # str, the AI's raw reply
    question_data = json.loads(content)                     # convert the JSON text into a dict
    return question_data


def play_quiz():
    name = input("Enter your name: ")   # str
    print(f"\nHi {name}! Answer each question by typing the option text exactly.\n")

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

        categories_played.add(q["category"])  # set automatically avoids duplicates

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
    sorted_board = sorted(leaderboard, key=lambda entry: entry[1], reverse=True)

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


def play_ai_round():
    """The online module: get a fresh question from the Groq AI instead of the CSV file."""
    print("\nContacting the Groq AI for a fresh question...\n")

    try:
        q = ask_groq_for_question()
    except requests.exceptions.HTTPError as e:
        print(f"Groq rejected the request (status {e.response.status_code}). Details:\n{e.response.text}\n")
        return
    except requests.exceptions.RequestException as e:
        print(f"Couldn't reach Groq — check your internet connection. Details: {e}\n")
        return
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Got a response, but couldn't understand it. Details: {e}\n")
        return

    name = input("Enter your name: ")  # str

    print(f"\n[AI-generated question]")
    print(q["question"])
    for i, option in enumerate(q["options"], start=1):
        print(f"  {i}. {option}")

    answer = input("Your answer: ").strip()  # str
    is_correct = answer.lower() == q["answer"].lower()  # bool

    if is_correct:
        print("Correct! The AI's question didn't stump you.\n")
        score = 1
    else:
        print(f"Wrong. The correct answer was: {q['answer']}\n")
        score = 0

    percentage = score * 100.0  # float
    categories_played.add(q.get("category", "AI"))  # set

    entry = (name, score, percentage)  # tuple, same shape as the regular leaderboard entries
    leaderboard.append(entry)
    print(f"Added to leaderboard: {entry}\n")


def main():
    while True:
        print("---- Quiz Game ----")
        print("1. Play quiz")
        print("2. Show leaderboard")
        print("3. Show categories played")
        print("4. Save leaderboard to file")
        print("5. Load leaderboard from file")
        print("6. Ask the AI (Groq) for a live question")
        print("7. Quit")
        choice = input("Choose an option (1-7): ")

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
            play_ai_round()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.\n")


if __name__ == "__main__":
    main()
