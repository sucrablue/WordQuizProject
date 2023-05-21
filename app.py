# coding: utf-8

from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

def load_flashcards(file):
    df = pd.read_excel(file)
    flashcards = df.to_dict('records')
    return flashcards

def get_multiple_choices(flashcards, correct_answer):
    incorrect_flashcards = [fc['Answer'] for fc in flashcards if fc['Answer'] != correct_answer]
    choices = [correct_answer] + random.sample(incorrect_flashcards, 3)
    random.shuffle(choices)
    return choices

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            flashcards = load_flashcards(file)
            random.shuffle(flashcards)
            session['flashcards'] = flashcards
            session['current_question'] = 0
            session['num_correct'] = 0
            session['incorrect_answers'] = []
            return redirect(url_for('quiz'))
        else:
            flash('Please upload an .xlsx file.', 'error')
            return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'flashcards' not in session:
        return redirect(url_for('index'))
    
    flashcards = session['flashcards']
    current_question = session['current_question']
    question = flashcards[current_question]['Question']
    answer = flashcards[current_question]['Answer']
    choices = get_multiple_choices(flashcards, answer)

    if request.method == 'POST':
        user_answer = request.form.get('user_answer', '').strip()

        if user_answer.lower() == 'stop':
            return redirect(url_for('results'))

        try:
            user_choice = choices[int(user_answer) - 1]
        except (ValueError, IndexError):
            flash("Invalid input. Please enter a number corresponding to one of the choices. Skipping this question.", 'error')
        else:
            if user_choice.strip().lower() == answer.strip().lower():
                flash("Correct!", 'success')
                session['num_correct'] += 1
            else:
                flash(f"Wrong. The correct answer is: {answer}", 'error')
                session['incorrect_answers'].append((question, user_choice, answer))

        session['current_question'] += 1
        if session['current_question'] >= len(session['flashcards']):
            return redirect(url_for('results'))

    return render_template('quiz.html', question=question, choices=choices)

@app.route('/results', methods=['GET', 'POST'])
def results():
    if 'flashcards' in session:
        num_questions = len(session['flashcards'])
        num_correct = session['num_correct']
        incorrect_answers = session['incorrect_answers']

        # Calculate the percentage of correct answers
        score_percentage = (num_correct / num_questions) * 100

        return render_template('results.html', num_correct=num_correct, num_questions=num_questions, score_percentage=score_percentage, incorrect_answers=incorrect_answers)
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
