from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_entry():
    content = request.json.get('content')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute("INSERT INTO journal (content, timestamp) VALUES (?, ?)", (content, timestamp))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/entries', methods=['GET'])
def get_entries():
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute("SELECT id, content, timestamp FROM journal ORDER BY id DESC")
    entries = c.fetchall()
    conn.close()
    return jsonify(entries)

if __name__ == '__main__':
    app.run(debug=True)
