# Quiz Game

A python quiz game that runs in the terminal. Questions are loaded from a csv file (questions.csv) instead of being typed straight into the code, so it's easy to add more questions without touching the program itself. You answer multiple choice trivia questions and it keeps track of your score, then saves it to a leaderboard file.

## How to run it
python quiz_game.py

## What it does
- Loads questions from questions.csv and picks 5 at random each round
- Keeps score as you go and shows your percentage at the end
- Shows a leaderboard sorted by highest score
- Shows which categories you've covered (no repeats)
- Can save your score to a file and load it back later

## Data types I used
- str - questions, options, player name
- int - score, number of questions
- float - percentage score
- bool - checking if an answer is correct
- list - the questions and the leaderboard
- dict - each question (question, options, answer, category)
- tuple - (name, score, percentage) for each leaderboard entry
- set - keeping track of categories played with no duplicates

Also used the csv module to read the questions file, and try/except for saving/loading the leaderboard, since everything read from a file comes back as text and has to be converted back to int/float.