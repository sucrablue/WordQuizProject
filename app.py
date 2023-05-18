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
    choices.sort()
    return choices

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.xlsx'):
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
    
    if request.method == 'POST':
        user_answer = request.form.get('user_answer', '').strip()

        if user_answer.lower() == 'stop':
            return redirect(url_for('results'))

        flashcards = session['flashcards']
        current_question = session['current_question']
        answer = flashcards[current_question]['Answer']
        choices = get_multiple_choices(flashcards, answer)

        try:
            user_choice = choices[int(user_answer) - 1]
        except (ValueError, IndexError):
            flash("Invalid input. Skipping this question.", 'error')
        else:
            if user_choice.strip().lower() == answer.strip().lower():
                flash("Correct!", 'success')
                session['num_correct'] += 1
            else:
                flash(f"Wrong. The correct answer is: {answer}", 'error')
                session['incorrect_answers'].append((flashcards[current_question]['Question'], user_choice, answer))

        session['current_question'] += 1
        if session['current_question'] >= len(session['flashcards']):
            return redirect(url_for('results'))

    return render_template('quiz.html', get_multiple_choices=get_multiple_choices)

@app.route('/results', methods=['GET', 'POST'])
def results():
    if 'flashcards' in session:
        num_questions = len(session['flashcards'])
        num_correct = session['num_correct']
        num_answered = session['current_question']

        # Calculate the percentage of correct answers
        if num_answered != 0:
            score_percentage = (num_correct / num_answered) * 100
        else:
            score_percentage = None

        return render_template('result.html', num_correct=num_correct, num_questions=num_questions, num_answered=num_answered, score_percentage=score_percentage)
    else:
        return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
