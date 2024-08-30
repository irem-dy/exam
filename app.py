from flask import Flask, render_template, request
import webbrowser
import threading
import time

app = Flask(__name__)

DB_PATH = 'db/scores.db'

def get_db_connection():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    answers = {
        'q1': request.form.get('q1', 'Belirtilmemiş'),
        'q2': request.form.get('q2', 'Belirtilmemiş'),
        'q3': request.form.get('q3', 'Belirtilmemiş'),
        'q4': request.form.get('q4', 'Belirtilmemiş'),
    }

    correct_answers = {
        'q1': 'option1',
        'q2': 'option1',
        'q3': 'option1',
        'q4': 'option1',
    }

    answer_text = {
        'option1': "Makine Öğrenimi Algoritmaları",
        'option2': "Web Geliştirme Araçları",
        'option3': "Veritabanı Yönetimi",
        'option4': "Görüntü ve Video İşleme",
        'option5': "Doğal Dil İşleme",
        'option6': "AI Framework'leri Kullanarak"
    }


    for key in correct_answers:
        if answers[key] == correct_answers[key]:
            score += 1
        if answers[key] in answer_text:
            answers[key] = answer_text[answers[key]]
        else:
            answers[key] = "Belirtilmemiş"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO scores (score, answers) VALUES (?, ?)', (score, str(answers)))
    conn.commit()
    conn.close()

    return render_template('result.html', score=score, answers=answers)

def open_browser():
    time.sleep(1) 
    webbrowser.open('http://127.0.0.1:5001')

if __name__ == '__main__':

    threading.Thread(target=open_browser).start()
    
    app.run(port=5001, debug=True)
