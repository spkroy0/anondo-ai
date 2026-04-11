import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='static')

# Groq API Configuration
API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    # Home page jekhane apnar details r button thakbe
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    # Chatbot er alada page (anondo.bro.bd/chat)
    return render_template('chat.html')

@app.route('/chat_api', methods=['POST'])
def chat_api():
    user_message = request.json.get("message", "")
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are Turmax AI, Anondo's friend. Speak in Banglish (Bengali using English letters)."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=10)
        bot_reply = response.json()["choices"][0]["message"]["content"]
    except:
        bot_reply = "Dost, server e ektu jhamela hosse. Pore try koro!"
        
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
