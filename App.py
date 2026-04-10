import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Groq API Configuration
API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

# চ্যাটবটকে শেখানো হচ্ছে সে কে এবং কীভাবে কথা বলবে
SYSTEM_INSTRUCTION = (
    "You are Turmax AI, a highly intelligent assistant created by Anondo. "
    "You are smart like ChatGPT. Speak in Bengali but ONLY use English/Latin letters (Banglish). "
    "Be friendly, funny, and helpful. You can answer anything."
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        data = request.json
        user_input = data.get("message", "")

        if not user_input:
            return jsonify({"reply": "Kisu to likho dost!"})

        # Groq API তে রিকোয়েস্ট পাঠানো হচ্ছে (ChatGPT এর মতো উত্তরের জন্য)
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.8, # একটু সৃজনশীল উত্তরের জন্য
            "max_tokens": 1024
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(URL, headers=headers, json=payload)
        result = response.json()

        if "choices" in result:
            bot_reply = result["choices"][0]["message"]["content"]
            return jsonify({"reply": bot_reply})
        else:
            return jsonify({"reply": "Dost, API te ektu jhamela hocche. Ektu por try koro."})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    # Render এর জন্য পোর্ট সেটআপ
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
