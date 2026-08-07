# Quiz Game

A python quiz game that runs in the terminal. Questions are loaded from a csv file (questions.csv), and there's also an online mode that asks the Groq AI to generate a fresh question live. You answer multiple choice trivia questions and it keeps track of your score, then saves it to a leaderboard file.

## How to run it
python quiz_game.py

If you get an error about "requests" not being installed, run this first:
pip install requests

## Setting up the online AI mode (optional)
The AI question mode uses the Groq API. To use it:
1. Get a free API key from console.groq.com
2. When the program asks for it, paste your key in (or set it as an environment variable called GROQ_API_KEY so you don't have to type it every time)

The rest of the game works completely fine without a key — this part is optional.

## What it does
- Loads questions from questions.csv and picks 5 at random each round (offline)
- Can also fetch a live AI-generated question from Groq (online)
- Keeps score as you go and shows your percentage at the end
- Shows a leaderboard sorted by highest score
- Shows which categories you've covered (no repeats)
- Can save your score to a file and load it back later

## Data types I used
- str - questions, options, player name, API key
- int - score, number of questions
- float - percentage score
- bool - checking if an answer is correct
- list - the questions and the leaderboard
- dict - each question (question, options, answer, category)
- tuple - (name, score, percentage) for each leaderboard entry
- set - keeping track of categories played with no duplicates

Also used the csv module to read the questions file, try/except for saving/loading and for handling network errors when calling Groq, and the json module to read Groq's response. Uses the requests library to call the Groq API (Python's built in urllib gets blocked by Groq's Cloudflare protection).