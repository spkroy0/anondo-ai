import os
import requests
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__, static_folder='static')
app.secret_key = "anondo_secret_key_2026"

# --- Groq API Configuration ---
# Tumi ekhon matro je key-ta dile oita ekhane boshanu hoyeche
API_KEY = "Gsk_tOW44UqXqHS06hwLJoXeWGdyb3FYcHAd9R12GG3tgoK9etu8Y2Dq"
URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    session['chat_history'] = [
        {"role": "system", "content": "You are Turmax AI, created by Anondo Kumar Roy. Speak in friendly Banglish."}
    ]
    return render_template('chat.html')

@app.route('/chat_api', methods=['POST'])
def chat_api():
    user_message = request.json.get("message", "")
    
    if 'chat_history' not in session:
        session['chat_history'] = [{"role": "system", "content": "You are Turmax AI. Speak in Banglish."}]

    history = session['chat_history']
    history.append({"role": "user", "content": user_message})

    # Groq er jonno payload
    payload = {
        "model": "llama-3.3-70b-versatile", # Groq-er shera model
        "messages": history,
        "temperature": 0.8,
        "max_tokens": 1024
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            bot_reply = response.json()["choices"][0]["message"]["content"]
            history.append({"role": "assistant", "content": bot_reply})
            
            # History control (memory limit)
            if len(history) > 12:
                session['chat_history'] = [history[0]] + history[-11:]
            else:
                session['chat_history'] = history
            
            session.modified = True
            return jsonify({"response": bot_reply})
        else:
            # API theke kono error ashle oita ekhane dhora porbe
            error_data = response.json()
            print(f"Groq API Error: {error_data}")
            return jsonify({"response": "Dost, API key-te ektu jhamela mone hochhe. Key-ta check koro."})

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"response": "Dost, connection error! Check your internet or server."})

# --- Other Routes ---
@app.route('/font')
def font_engine():
    return render_template('font.html')

@app.route('/py-editor')
def py_editor():
    return render_template('editor.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
