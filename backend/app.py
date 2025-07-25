from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import openai
import os
import random
import requests

# Load configurations
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = os.urandom(24)  # For session management
openai.api_key = app.config['OPENAI_API_KEY']

# Set up MongoDB
client = MongoClient(app.config['MONGO_URI'])
db = client['quizzcrakerz']
users_collection = db['users']
subjects_collection = db['subjects']
questions_collection = db['questions']

# Fetching questions using Open Trivia DB API
def fetch_questions(subject):
    # Updated category codes for Open Trivia DB for better subject specificity
    categories = {
        'Computer Networks': 17,  # Science & Nature (closest)
        'Data Structures': 18,    # Computers
        'Database Management Systems': 18,  # Computers
        'Web Development': 18,    # Computers
        'Programming Languages': 18,  # Computers
        'Operating Systems': 18,  # Computers
        'Software Engineering': 18,  # Computers
        'Mathematics for Computing': 19,  # Mathematics
        'OOP': 18,                # Computers
        'Computer Graphics': 18   # Computers
    }
    category_id = categories.get(subject, 18)

    # API call to Open Trivia DB to fetch questions for the category
    url = f"https://opentdb.com/api.php?amount=10&category={category_id}&type=multiple"
    response = requests.get(url)
    data = response.json()
    
    if data['response_code'] == 0:
        questions = []
        for q in data['results']:
            questions.append({
                'question': q['question'],
                'options': q['incorrect_answers'] + [q['correct_answer']],
                'correct': q['correct_answer']
            })
        random.shuffle(questions)  # Shuffle the options for randomness
        return questions
    else:
        return []

# Helper function to check if user is logged in
def is_logged_in():
    return 'user_id' in session

# Route for Frontpage
@app.route('/')
def frontpage():
    return render_template('frontpage.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Here you can handle form submission, e.g., save contact info or send email
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # For now, just redirect back to contact page with a success message or handle as needed
        return render_template('contact.html', success=True)
    return render_template('contact.html')

@app.route('/service')
def service():
    return render_template('service.html')

# Route for Sign Up and Login Page
@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form['action']  # Check if user is logging in or signing up
        email = request.form['email']
        password = request.form['password']

        if action == 'login':
            # Handle login
            user = users_collection.find_one({'email': email})
            if user and check_password_hash(user['password'], password):
                # Store user session
                session['user_id'] = str(user['_id'])  # Convert ObjectId to string
                session['user'] = email  # Store email or username for display
                return redirect(url_for('dashboard'))
            else:
                # Redirect to the login page with an error
                return render_template('index.html', error="Invalid email or password.")

        elif action == 'signup':
            # Handle signup
            existing_user = users_collection.find_one({'email': email})
            if existing_user:
                return render_template('index.html', error="Email already exists. Please choose a different one.")
            else:
                # Hash the password and save the user to MongoDB
                hashed_password = generate_password_hash(password)
                users_collection.insert_one({'email': email, 'password': hashed_password})
                return redirect(url_for('index'))  # Redirect to login after signup

    return render_template('index.html')


# Route for Dashboard page
@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('index'))
    return render_template('dashboard.html')

# Route for Subject Selection page
@app.route('/subject_selection')
def subject_selection():
    if not is_logged_in():
        return redirect(url_for('index'))
    return render_template('subject_selection.html')

# Route for Quiz page
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if not is_logged_in():
        return redirect(url_for('index'))
    if request.method == 'POST':
        # Handle quiz submission here
        submitted_answers = request.form.to_dict()
        subject = submitted_answers.get('subject', 'Computer Networks')
        questions = session.get('questions')

        if not questions:
            questions = fetch_questions(subject)

        score = 0
        total = len(questions)

        # Calculate score by comparing submitted answers with correct answers
        for i, question in enumerate(questions):
            user_answer = submitted_answers.get(f'question_{i}')
            if user_answer == question['correct']:
                score += 1

        # Store score and total in session to pass to result page
        session['score'] = score
        session['total'] = total
        session['subject'] = subject

        # Clear questions from session after scoring
        session.pop('questions', None)

        return redirect(url_for('result'))
    # For GET request, fetch questions for a default or selected subject
    subject = request.args.get('subject', 'Computer Networks')
    session['subject'] = subject
    questions = fetch_questions(subject)
    session['questions'] = questions
    time_limit = 2  # 2 minutes time limit for quiz
    return render_template('quiz.html', questions=questions, subject=subject, time_limit=time_limit)

# Route for Result page
@app.route('/result')
def result():
    if not is_logged_in():
        return redirect(url_for('index'))
    score = session.get('score')
    total = session.get('total')
    if score is None or total is None:
        return redirect(url_for('dashboard'))
    return render_template('result.html', score=score, total=total)

# Route for Our Teams page
@app.route('/our_teams')
def our_teams():
    return render_template('our_teams.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    from os import environ
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)))