import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Groq API Configuration
API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

# System Instruction (আপনার দেওয়া সেই বাংলিশ ইনস্ট্রাকশন)
system_instruction = "You are Turmax AI, Anondo's friend. Speak in Bengali but ONLY use English/Latin letters (Banglish). Do not use Bengali script."

@app.route('/')
def home():
    return render_template('index.html') # আপনার হোম পেজ

@app.route('/chat')
def chat_page():
    return render_template('chat.html') # চ্যাটবট পেজ

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        data = request.json
        user_input = data.get("message", "")

        # Groq API Call লজিক
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.7
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
            # যদি এপিআই এরর দেয়
            error_msg = result.get("error", {}).get("message", "API Error")
            return jsonify({"reply": f"Error: {error_msg}"})

    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"})

if __name__ == "__main__":
    app.run()
