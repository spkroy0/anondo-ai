import os
import requests
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__, static_folder='static')
app.secret_key = "anondo_secret_key_2026"

# Groq API Configuration
API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    session['chat_history'] = [
        {"role": "system", "content": "You are Turmax AI, a assistant created by Anondo Kumar Roy. Speak in friendly Banglish."}
    ]
    return render_template('chat.html')

@app.route('/chat_api', methods=['POST'])
def chat_api():
    user_message = request.json.get("message", "")
    if 'chat_history' not in session:
        session['chat_history'] = [{"role": "system", "content": "You are Turmax AI. Speak in Banglish."}]

    history = session['chat_history']
    history.append({"role": "user", "content": user_message})

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": history,
        "temperature": 0.8,
        "max_tokens": 1024
    }
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=15)
        bot_reply = response.json()["choices"][0]["message"]["content"]
        history.append({"role": "assistant", "content": bot_reply})
        session['chat_history'] = [history[0]] + history[-11:] if len(history) > 12 else history
    except:
        bot_reply = "Dost, ektu error hoise. Abar bolo?"
        
    return jsonify({"response": bot_reply})

# --- ফন্ট ইঞ্জিন রাউট ---
@app.route('/font')
def font_engine():
    return render_template('font.html')

# --- পাইথন এডিটর রাউট (নতুন যোগ করা হলো) ---
@app.route('/py-editor')
def py_editor():
    # এটি আপনার templates ফোল্ডারের editor.html ফাইলটিকে দেখাবে
    return render_template('editor.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
