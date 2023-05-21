# coding: utf-8

import pandas as pd
import random
import os

REQUIRED_COLUMNS = ['Question', 'Answer'] # 必要な列名をリストとして定義
NUM_CHOICES = 4 # 選択肢の数を定義

# Excelファイルからフラッシュカードをロード
def load_flashcards(file_name):
    try:
        df = pd.read_excel(file_name) # pandasを使ってExcelファイルを読み込む

        if not all(column in df.columns for column in REQUIRED_COLUMNS): # ファイルに必要な列（'Question', 'Answer'）が全て存在することを確認
            print("The file must have 'Question' and 'Answer' columns.")
            return None

        flashcards = df[REQUIRED_COLUMNS].to_dict('records') # 必要な列だけを含む辞書を作成
        return flashcards

    except Exception as e:
        print(f"Error loading file: {e}")
        return None

# 正しい答えと他の選択肢を取得
def get_multiple_choices(flashcards, correct_answer): 
    incorrect_flashcards = [fc['Answer'] for fc in flashcards if fc['Answer'] != correct_answer] # flashcardsの中から正しい答え以外のものを選ぶ
    choices = [correct_answer] + random.sample(incorrect_flashcards, NUM_CHOICES - 1) # 正解と誤答を混ぜた選択肢を作成
    random.shuffle(choices) # 選択肢の順序をシャッフル
    return choices

# 問題と選択肢を表示
def display_question_and_choices(idx, num_questions, question, choices):
    print(f"Question {idx}/{num_questions}: {question}")
    for i, choice in enumerate(choices, start=1): # 選択肢を順番に表示
        print(f"{i}. {choice}")

# クイズを実施
def quiz_flashcards(flashcards):
    num_correct = 0
    num_questions = len(flashcards)
    random.shuffle(flashcards) # flashcardsの順序をシャッフル
    incorrect_answers = []
    current_question = 0

    for idx, flashcard in enumerate(flashcards, start=1):
        question = flashcard['Question']
        answer = flashcard['Answer']
        choices = get_multiple_choices(flashcards, answer) # 正解と他の選択肢を取得

        display_question_and_choices(idx, num_questions, question, choices) # 質問と選択肢を表示

        user_answer = input("Your answer (or type 'stop' to end the quiz): ") # 回答を取得

        if user_answer.strip().lower() == 'stop':
            break

        current_question += 1

        try:
            user_choice = choices[int(user_answer) - 1] # 選んだ選択肢を取得
        except (ValueError, IndexError):
            print("Invalid input. Skipping this question.")
            continue

        if user_choice.strip().lower() == answer.strip().lower(): # 選んだ選択肢が正解と一致するか確認
            print("Correct!")
            num_correct += 1
        else:
            print(f"Wrong. The correct answer is: {answer}")
            incorrect_answers.append((question, user_choice, answer))
        print()

    print(f"Your score: {num_correct}/{current_question}")

    if incorrect_answers: # 間違えた問題を表示
        print("\nReview your incorrect answers:\n")
        for question, user_choice, correct_answer in incorrect_answers:
            print(f"Question: {question}\nYour answer: {user_choice}\nCorrect answer: {correct_answer}\n")

# エラー処理
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

# Excelファイルを選択
def select_excel_file():
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.xlsx')] # ディレクトリにあるExcelファイルをリスト化

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
        if flashcards:
            quiz_flashcards(flashcards)
        else:
            print("Failed to load flashcards from the file. Please check the file and try again.")
    else:
        print("Please add an Excel file to the current directory and try again.")
