import os
import requests
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__, static_folder='static')
app.secret_key = "anondo_secret_key_2026"

# --- OpenRouter (Qwen AI) Configuration ---
API_KEY = "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"
URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    session['chat_history'] = [
        {"role": "system", "content": "You are Turmax AI, a smart assistant created by Anondo Kumar Roy. Speak in friendly Banglish."}
    ]
    return render_template('chat.html')

@app.route('/chat_api', methods=['POST'])
def chat_api():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Kisu bolbe to, dost?"})

    if 'chat_history' not in session:
        session['chat_history'] = [{"role": "system", "content": "You are Turmax AI. Speak in Banglish."}]

    history = session['chat_history']
    history.append({"role": "user", "content": user_message})

    # OpenRouter Payload (Qwen 2.5 72B use kora hoyeche, eta khub powerful)
    payload = {
        "model": "alibabacloud/qwen-2.5-72b-instruct", 
        "messages": history,
        "temperature": 0.7
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost:5000", # OpenRouter er jonno eta dorkar
        "X-Title": "Turmax AI",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            bot_reply = response.json()["choices"][0]["message"]["content"]
            history.append({"role": "assistant", "content": bot_reply})
            
            # History control (Memory limit)
            if len(history) > 12:
                session['chat_history'] = [history[0]] + history[-11:]
            else:
                session['chat_history'] = history
                
            session.modified = True
            return jsonify({"response": bot_reply})
        else:
            error_data = response.json()
            print(f"OpenRouter Error: {error_data}")
            return jsonify({"response": f"Dost, OpenRouter error dise: {response.status_code}. Key-te balance ase to?"})

    except Exception as e:
        return jsonify({"response": f"Server jhamela: {str(e)}"})

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
