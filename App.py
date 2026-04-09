import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are Anondo's Friend. Speak in Banglish (Bengali with English letters)."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }
    response = requests.post(URL, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }, json=data)
    return jsonify(response.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
