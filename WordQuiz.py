import pandas as pd
import random
import os

def load_flashcards(file_name):
    df = pd.read_excel(file_name)
    flashcards = df.to_dict('records')
    return flashcards

def get_multiple_choices(flashcards, correct_answer):
    incorrect_flashcards = [fc['Answer'] for fc in flashcards if fc['Answer'] != correct_answer]
    choices = [correct_answer] + random.sample(incorrect_flashcards, 3)
    choices.sort()
    return choices

def display_question_and_choices(idx, num_questions, question, choices):
    print(f"Question {idx}/{num_questions}: {question}")
    for i, choice in enumerate(choices, start=1):
        print(f"{i}. {choice}")

def quiz_flashcards(flashcards):
    num_correct = 0
    num_questions = len(flashcards)
    random.shuffle(flashcards)
    incorrect_answers = []

    for idx, flashcard in enumerate(flashcards, start=1):
        question = flashcard['Question']
        answer = flashcard['Answer']
        choices = get_multiple_choices(flashcards, answer)

        display_question_and_choices(idx, num_questions, question, choices)
        user_answer = input("Your answer (or type 'stop' to end the quiz): ")

        if user_answer.strip().lower() == 'stop':
            break

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

    print(f"Your score: {num_correct}/{idx - 1}")

    if incorrect_answers:
        print("\nReview your incorrect answers:")
        for question, user_choice, correct_answer in incorrect_answers:
            print(f"Question: {question}\nYour answer: {user_choice}\nCorrect answer: {correct_answer}\n")

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
        quiz_flashcards(flashcards)
    else:
        print("Please add an Excel file to the current directory and try again.")
