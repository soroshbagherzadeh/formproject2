from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = 'mydata.db'

# ایجاد دیتابیس در صورت عدم وجود
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

@app.route('/api', methods=['POST'])
def handle_request():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    action = data.get('action')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    # عملیات ثبت‌نام
    if action == 'register':
        if user:
            result = {"message": "⚠️ این نام کاربری قبلاً ثبت شده است."}
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            result = {"message": "✅ ثبت‌نام با موفقیت انجام شد."}

    # عملیات ورود
    elif action == 'login':
        if user:
            if user[0] == password:
                result = {"message": "✅ ورود موفق بود."}
            else:
                result = {"message": "❌ رمز عبور اشتباه است."}
        else:
            result = {"message": "❌ ابتدا ثبت‌نام کنید."}

    # عملیات نامعتبر
    else:
        result = {"message": "❌ عملیات نامعتبر."}

    conn.close()
    return jsonify(result)
@app.route('/')
def serve_form():
    return send_from_directory('.', 'form.html')
if __name__ == '__main__':
    app.run(debug=True)
    
