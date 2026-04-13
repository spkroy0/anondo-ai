import os
import requests
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__, static_folder='static')
app.secret_key = "anondo_secret_key_2026"

# --- xAI (Grok) API Configuration ---
# Note: Key ta ekhane hardcoded, kintu pore environment variable e move kora bhalo
API_KEY = "xai-XQcI0Hb9qhup4LOQbYYZBhUpW1hrYtMumGEGgSaCBkl3iXYei7u26tA5SP7LcNF3UZEBN46QhDdijFE8"
URL = "https://api.x.ai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    # Fresh session start
    session['chat_history'] = [
        {"role": "system", "content": "You are Turmax AI, a friendly assistant created by Anondo Kumar Roy. Speak in natural Banglish."}
    ]
    return render_template('chat.html')

@app.route('/chat_api', methods=['POST'])
def chat_api():
    user_message = request.json.get("message", "")
    
    if 'chat_history' not in session:
        session['chat_history'] = [
            {"role": "system", "content": "You are Turmax AI. Speak in Banglish."}
        ]

    history = session['chat_history']
    history.append({"role": "user", "content": user_message})

    # xAI Payload
    payload = {
        "model": "grok-beta",  # xAI er standard model name
        "messages": history,
        "temperature": 0.8,
        "stream": False
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=20)
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            bot_reply = result["choices"][0]["message"]["content"]
            
            # History update
            history.append({"role": "assistant", "content": bot_reply})
            
            # Keep only last 10-12 messages for memory efficiency
            if len(history) > 12:
                session['chat_history'] = [history[0]] + history[-11:]
            else:
                session['chat_history'] = history
                
            session.modified = True
        else:
            print(f"Error from xAI: {response.text}")
            bot_reply = f"Dost, xAI theke error ashche (Status: {response.status_code}). Key ta check koro?"

    except Exception as e:
        print(f"System Error: {e}")
        bot_reply = "Dost, ektu error hoise connection-e. Abar bolo?"
        
    return jsonify({"response": bot_reply})

# --- Font Engine Route ---
@app.route('/font')
def font_engine():
    return render_template('font.html')

# --- Python Editor Route ---
@app.route('/py-editor')
def py_editor():
    return render_template('editor.html')

if __name__ == "__main__":
    # Deployment support
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
