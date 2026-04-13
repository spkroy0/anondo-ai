import os
import requests
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__, static_folder='static')

# Secret key-ta environment variable theke nawa safe
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "69750e87ea9699cf914b0bff8e4e68a802f89ed4de3a5559")

# Groq API Configuration (Render dashboard theke nibe)
API_KEY = os.environ.get("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    # Chat history reset for new session
    session['chat_history'] = [
        {"role": "system", "content": "You are Turmax AI, a smart assistant created by Anondo Kumar Roy. Speak in friendly Banglish."}
    ]
    return render_template('chat.html')

@app.route('/chat_api', methods=['POST'])
def chat_api():
    if not API_KEY:
        return jsonify({"response": "🚨 API Key set kora nai! Render Dashboard-e GROQ_API_KEY add koro."})

    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Kisu bolo, dost!"})

    if 'chat_history' not in session:
        session['chat_history'] = [{"role": "system", "content": "You are Turmax AI. Speak in Banglish."}]

    history = session['chat_history']
    history.append({"role": "user", "content": user_message})

    # Groq Payload
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": history,
        "temperature": 0.8,
        "max_tokens": 1024
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            bot_reply = result["choices"][0]["message"]["content"]
            
            history.append({"role": "assistant", "content": bot_reply})
            
            # Context window limit (Keep last 12 messages)
            if len(history) > 12:
                session['chat_history'] = [history[0]] + history[-11:]
            else:
                session['chat_history'] = history
                
            session.modified = True
            return jsonify({"response": bot_reply})
        else:
            error_info = response.json()
            print(f"Groq Error: {error_info}")
            return jsonify({"response": f"❌ Groq API Error: {response.status_code}"})

    except Exception as e:
        return jsonify({"response": f"⚠️ System error: {str(e)}"})

# --- Other Routes ---
@app.route('/font')
def font_engine():
    return render_template('font.html')

@app.route('/py-editor')
def py_editor():
    return render_template('editor.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
