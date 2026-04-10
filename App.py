import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# API Configuration (আপনার দেওয়া API Key)
API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

# চ্যাটের মেমোরি রাখার জন্য (সার্ভার রিস্টার্ট দিলে এটি ক্লিয়ার হবে)
chat_history = [
    {"role": "system", "content": "You are Turmax AI, Anondo's friend. Speak in Bengali but ONLY use English/Latin letters (Banglish). Do not use Bengali script."}
]

@app.route('/')
def home():
    return render_template('index.html') # আপনার বর্তমান হোম পেজ

@app.route('/chat')
def chat_page():
    return render_template('chat.html') # আপনার চ্যাটবট পেজ

@app.route('/get_response', methods=['POST'])
def get_response():
    global chat_history
    try:
        user_input = request.json.get("message")

        if user_input.lower() == "clear":
            chat_history = [chat_history[0]]
            return jsonify({"reply": "AI: Memory clear kora hoyeche."})

        chat_history.append({"role": "user", "content": user_input})

        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": chat_history,
            "temperature": 0.7
        }

        response = requests.post(URL, headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }, json=data)

        result = response.json()

        if "choices" in result:
            answer = result["choices"][0]["message"]["content"]
            chat_history.append({"role": "assistant", "content": answer})

            # Context limit: শেষ ১০টি মেসেজ মনে রাখবে
            if len(chat_history) > 10:
                chat_history = [chat_history[0]] + chat_history[-9:]
            
            return jsonify({"reply": answer})
        else:
            return jsonify({"reply": "Error: API connection fail hoyeche."})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run()
