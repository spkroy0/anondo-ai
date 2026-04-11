import os
import requests
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__, static_folder='static')
app.secret_key = "anondo_secret_key_2026" # সেশন সেভ রাখার জন্য

# Groq API Configuration
API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    # চ্যাট পেজে ঢুকলে পুরনো মেমোরি ক্লিয়ার হয়ে যাবে ফ্রেশ চ্যাটের জন্য
    session['chat_history'] = [
        {"role": "system", "content": "You are Turmax AI, a super-intelligent assistant created by Anondo Kumar Roy. Speak in friendly Banglish (Bengali with English letters). Be creative, funny, and smart like ChatGPT."}
    ]
    return render_template('chat.html')

@app.route('/chat_api', methods=['POST'])
def chat_api():
    user_message = request.json.get("message", "")
    
    if 'chat_history' not in session:
        session['chat_history'] = [
            {"role": "system", "content": "You are Turmax AI, Anondo's smart friend. Speak in Banglish."}
        ]

    # ইউজারের মেসেজ মেমোরিতে যোগ করা
    history = session['chat_history']
    history.append({"role": "user", "content": user_message})

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": history,
        "temperature": 0.8, # একটু বাড়িয়ে দিলাম যাতে উত্তর বৈচিত্র্যময় হয়
        "max_tokens": 1024
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=15)
        response_data = response.json()
        bot_reply = response_data["choices"][0]["message"]["content"]
        
        # এআই-এর উত্তর মেমোরিতে সেভ করা যাতে পরেরবার সে এটা মনে রাখে
        history.append({"role": "assistant", "content": bot_reply})
        
        # মেমোরি লিমিট (সর্বশেষ ১০টা মেসেজ মনে রাখবে যাতে স্লো না হয়)
        if len(history) > 12:
            session['chat_history'] = [history[0]] + history[-11:]
        else:
            session['chat_history'] = history

    except Exception as e:
        bot_reply = "Dost, matha ektu jam hoye gese (API Error). Abar bolo to?"
        
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
