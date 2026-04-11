import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='static')

# আপনার দেওয়া Groq API কনফিগারেশন
API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    
    if not user_message:
        return jsonify({"response": "Kichu to likho bhai!"})

    # সিস্টেম ইন্সট্রাকশন (আপনার টার্মিনাল কোড অনুযায়ী)
    instruction = "You are Turmax AI, Anondo's friend. Speak in Bengali but ONLY use English/Latin letters (Banglish). Do not use Bengali script."

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": instruction},
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
        result = response.json()
        
        if "choices" in result:
            bot_reply = result["choices"][0]["message"]["content"]
        else:
            bot_reply = "API Connection fail hoyeche dost!"
    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
