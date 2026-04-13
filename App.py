import os
import requests
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__, static_folder='static')
app.secret_key = "anondo_secret_key_2026"

# --- SambaNova API Configuration ---
API_KEY = "Ef0cc8f3-fd4c-4158-a3ab-1229e2cd2f3e" # Tomar dewa key
URL = "https://api.sambanova.ai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    session['chat_history'] = [
        {"role": "system", "content": "You are Turmax AI, a friendly assistant created by Anondo Kumar Roy. Speak in natural Banglish."}
    ]
    return render_template('chat.html')

@app.route('/chat_api', methods=['POST'])
def chat_api():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Kisu to bolo, dost!"})

    if 'chat_history' not in session:
        session['chat_history'] = [{"role": "system", "content": "You are Turmax AI. Speak in Banglish."}]

    history = session['chat_history']
    history.append({"role": "user", "content": user_message})

    # SambaNova Payload
    payload = {
        "model": "Meta-Llama-3.1-70B-Instruct", # SambaNova-r popular model
        "messages": history,
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            bot_reply = response.json()["choices"][0]["message"]["content"]
            history.append({"role": "assistant", "content": bot_reply})
            
            # History control (Memory)
            if len(history) > 12:
                session['chat_history'] = [history[0]] + history[-11:]
            else:
                session['chat_history'] = history
                
            session.modified = True
            return jsonify({"response": bot_reply})
        else:
            error_info = response.json()
            print(f"SambaNova Error: {error_info}")
            return jsonify({"response": f"Dost, SambaNova theke error ashche: {response.status_code}"})

    except Exception as e:
        return jsonify({"response": f"System error hoise: {str(e)}"})

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
