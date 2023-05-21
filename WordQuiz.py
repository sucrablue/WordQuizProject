# coding: utf-8

import pandas as pd
import random
import os

# These are the required columns in the Excel file
REQUIRED_COLUMNS = ['Question', 'Answer']
# This determines the number of multiple-choice options presented to the user for each question
NUM_CHOICES = 4

# Load the flashcards from an Excel file
def load_flashcards(file_name):
    try:
        df = pd.read_excel(file_name)
        # Check if the file has all the required columns
        if not all(column in df.columns for column in REQUIRED_COLUMNS):
            print("The file must have 'Question' and 'Answer' columns.")
            return None
        flashcards = df[REQUIRED_COLUMNS].to_dict('records')
        return flashcards
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

# Given a list of flashcards and a correct answer, this function generates multiple choices (1 correct and 3 incorrect)
def get_multiple_choices(flashcards, correct_answer):
    incorrect_flashcards = [fc['Answer'] for fc in flashcards if fc['Answer'] != correct_answer]
    choices = [correct_answer] + random.sample(incorrect_flashcards, NUM_CHOICES - 1)
    random.shuffle(choices)
    return choices

# Display a question and its choices
def display_question_and_choices(idx, num_questions, question, choices):
    print(f"Question {idx}/{num_questions}: {question}")
    for i, choice in enumerate(choices, start=1):
        print(f"{i}. {choice}")

def quiz_flashcards(flashcards):
    num_correct = 0
    num_questions = len(flashcards)
    random.shuffle(flashcards)
    incorrect_answers = []
    
    # Add a new variable to keep track of the current question number
    current_question = 0

    for idx, flashcard in enumerate(flashcards, start=1):
        question = flashcard['Question']
        answer = flashcard['Answer']
        choices = get_multiple_choices(flashcards, answer)

        display_question_and_choices(idx, num_questions, question, choices)
        user_answer = input("Your answer (or type 'stop' to end the quiz): ")

        if user_answer.strip().lower() == 'stop':
            break

        # Increment the current question number after a 'stop' has not been received
        current_question += 1

        try:
            user_choice = choices[int(user_answer) - 1]
        except (ValueError, IndexError):
            print("Invalid input. Skipping this question.")
            continue

        if user_choice.strip().lower() == answer.strip().lower():
            print("Correct!")
            num_correct += 1
        else:
            print(f"Wrong. The correct answer is: {answer}")
            incorrect_answers.append((question, user_choice, answer))
        print()

    # Use current_question instead of idx - 1
    print(f"Your score: {num_correct}/{current_question}")

    if incorrect_answers:
        print("\nReview your incorrect answers:")
        for question, user_choice, correct_answer in incorrect_answers:
            print(f"Question: {question}\nYour answer: {user_choice}\nCorrect answer: {correct_answer}\n")

# Validate the user's input to make sure it is a valid number within the correct range
def validate_user_input(user_input, max_valid):
    try:
        user_choice = int(user_input)
        if 1 <= user_choice <= max_valid:
            return user_choice
        else:
            print(f"Invalid selection. Please choose a number between 1 and {max_valid}.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

# Print the results of the quiz and save them to a text file
def print_and_save_results(num_correct, num_questions, incorrect_answers):
    print(f"Your score: {num_correct}/{num_questions}")

    if incorrect_answers:
        print("\nReview your incorrect answers:")
        for question, user_choice, correct_answer in incorrect_answers:
            print(f"Question: {question}\nYour answer: {user_choice}\nCorrect answer: {correct_answer}\n")

    with open('quiz_results.txt', 'w') as f:
        f.write(f"Your score: {num_correct}/{num_questions}\n")
        if incorrect_answers:
            f.write("\nReview your incorrect answers:\n")
            for question, user_choice, correct_answer in incorrect_answers:
                f.write(f"Question: {question}\nYour answer: {user_choice}\nCorrect answer: {correct_answer}\n")

def select_excel_file():
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.xlsx')]

    if not files:
        print("No Excel files found in the current directory.")
        return None

    if len(files) == 1:
        return files[0]

    print("Please select an Excel file to use for the quiz:")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")

    while True:
        try:
            user_selection = int(input("Enter the number of the file you want to use: ")) - 1
            if 0 <= user_selection < len(files):
                return files[user_selection]
            else:
                print("Invalid selection. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    file_name = select_excel_file()
    if file_name:
        flashcards = load_flashcards(file_name)
        # Add a check to ensure flashcards is not None
        if flashcards:
            quiz_flashcards(flashcards)
        else:
            print("Failed to load flashcards from the file. Please check the file and try again.")
    else:
        print("Please add an Excel file to the current directory and try again.")
