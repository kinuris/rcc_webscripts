import sqlite3
import json

from database import resibot

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/helloworld')
def index():
    return "Hello, World! ver 0.0.2"

# Endpoint to GET the state for a specific user
@app.route('/state/<chat_id>', methods=['GET'])
def get_state(chat_id):
    conn = resibot.get_conn()
    record = conn.execute("SELECT * FROM telegram_receipts WHERE chatId = ?", (chat_id,)).fetchone()
    conn.close()
    if record is None:
        return jsonify({"error": "No state found for this user"}), 404
    return jsonify(dict(record))

# Endpoint to CREATE or UPDATE a user's state
@app.route('/state', methods=['POST'])
def set_state():
    data = request.get_json()
    chat_id = data['chatId']
    state = data['state']
    receipt_json = json.dumps(data['receipt_json']) # Ensure it's a JSON string

    conn = resibot.get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO telegram_receipts (chatId, state, receipt_json) VALUES (?, ?, ?)",
        (chat_id, state, receipt_json)
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 200

# Endpoint to DELETE a user's state
@app.route('/state/<chat_id>', methods=['DELETE'])
def delete_state(chat_id):
    conn = resibot.get_conn()
    conn.execute("DELETE FROM telegram_receipts WHERE chatId = ?", (chat_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    resibot.setup_resibot_database()