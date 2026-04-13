import os
import requests
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__, static_folder='static')
app.secret_key = "anondo_secret_key_2026"

# --- Google Gemini API Configuration ---
API_KEY = "AIzaSyBT4I0orDRN_NCFFVUhzrCK0opWFEgO5pc"
# Gemini 1.5 Flash use kora hoyeche (Fast and Free)
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    # Gemini uses a slightly different history structure
    session['chat_history'] = [
        {"role": "user", "parts": [{"text": "You are Turmax AI, created by Anondo Kumar Roy. Always reply in friendly Banglish."}]},
        {"role": "model", "parts": [{"text": "Thik ache dost! Ami Turmax AI, ready!"}]}
    ]
    return render_template('chat.html')

@app.route('/chat_api', methods=['POST'])
def chat_api():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Kisu bolo!"})

    if 'chat_history' not in session:
        session['chat_history'] = []

    history = session['chat_history']
    
    # User message add kora
    history.append({"role": "user", "parts": [{"text": user_message}]})

    # Gemini Payload format
    payload = {
        "contents": history,
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 1024,
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            # Gemini response extract kora
            bot_reply = result['candidates'][0]['content']['parts'][0]['text']
            
            # History update
            history.append({"role": "model", "parts": [{"text": bot_reply}]})
            
            # Control history size (Gemini context window boro, but session optimized rakha bhalo)
            if len(history) > 15:
                session['chat_history'] = history[-15:]
            else:
                session['chat_history'] = history
                
            session.modified = True
            return jsonify({"response": bot_reply})
        else:
            print(f"Gemini Error: {response.text}")
            return jsonify({"response": f"Dost, Google AI error dise: {response.status_code}. Key block hole notun key generate koro."})

    except Exception as e:
        return jsonify({"response": f"System error: {str(e)}"})

@app.route('/font')
def font_engine():
    return render_template('font.html')

@app.route('/py-editor')
def py_editor():
    return render_template('editor.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
