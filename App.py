import os
import requests
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__, static_folder='static')

# GitHub-e push korar jonno amra environment variable use korbo
# Jodi Render-e FLASK_SECRET_KEY set na koro, tobe nicher default string-ta kaj korbe
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "69750e87ea9699cf914b0bff8e4e68a802f89ed4de3a5559")

# Gemini API Key (Render dashboard e boshabe)
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    # Gemini history setup
    session['chat_history'] = [
        {"role": "user", "parts": [{"text": "You are Turmax AI, created by Anondo Kumar Roy. Always reply in friendly Banglish."}]},
        {"role": "model", "parts": [{"text": "Thik ache dost! Ami Turmax AI, ready!"}]}
    ]
    return render_template('chat.html')

@app.route('/chat_api', methods=['POST'])
def chat_api():
    if not API_KEY:
        return jsonify({"response": "🚨 API Key set kora nai! Render Dashboard theke Environment Variable add koro."})

    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Kisu bolo!"})

    if 'chat_history' not in session:
        session['chat_history'] = []

    history = session['chat_history']
    history.append({"role": "user", "parts": [{"text": user_message}]})

    # Gemini API URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": history,
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 1024,
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            bot_reply = result['candidates'][0]['content']['parts'][0]['text']
            
            history.append({"role": "model", "parts": [{"text": bot_reply}]})
            
            # Context window size limit (last 15)
            if len(history) > 15:
                session['chat_history'] = history[-15:]
            else:
                session['chat_history'] = history
                
            session.modified = True
            return jsonify({"response": bot_reply})
        else:
            return jsonify({"response": f"Dost, Google AI error dise: {response.status_code}. Key ta check koro."})

    except Exception as e:
        return jsonify({"response": f"System error: {str(e)}"})

# Other routes...
@app.route('/font')
def font_engine():
    return render_template('font.html')

@app.route('/py-editor')
def py_editor():
    return render_template('editor.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
