import os
import sys
import sqlite3
import uuid
from flask import Flask, request, jsonify

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import send_single_email

app = Flask(__name__)

# Connect to SQLite database to store API keys
def init_db():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'api_keys.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY,
            api_key TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Generate a new API key
@app.route('/generate_api_key', methods=['POST'])
def generate_api_key():
    api_key = str(uuid.uuid4())
    db_path = os.path.join(os.path.dirname(__file__), '..', 'api_keys.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO api_keys (api_key) VALUES (?)", (api_key,))
    conn.commit()
    conn.close()
    return jsonify({"api_key": api_key})

# Authenticate API key
def authenticate(api_key):
    db_path = os.path.join(os.path.dirname(__file__), '..', 'api_keys.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT api_key FROM api_keys WHERE api_key = ?", (api_key,))
    key = c.fetchone()
    conn.close()
    return key is not None

# Endpoint to send email
@app.route('/send_email', methods=['POST'])
def api_send_email():
    api_key = request.headers.get('Authorization')
    if not api_key or not authenticate(api_key.split("Bearer ")[-1]):
        return jsonify({"error": "Invalid API Key"}), 403

    data = request.json
    subject = data.get('subject')
    recipient = data.get('recipient')
    html_content = data.get('html_content')

    if not subject or not recipient or not html_content:
        return jsonify({"error": "Missing email data"}), 400

    # Send the email using the existing function
    success = send_single_email(subject, recipient, html_content)
    if success:
        return jsonify({"message": "Email sent successfully"}), 200
    else:
        return jsonify({"error": "Failed to send email"}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)