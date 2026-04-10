import os
from flask import Flask, render_template, request, jsonify
import requests

# Flask app initialization
# এখানে template_folder উল্লেখ করে দেওয়া হয়েছে যাতে templates ফোল্ডার থেকে ফাইল খুঁজে পায়
app = Flask(__name__, template_folder='templates')

# API details for Groq (Llama 3.3)
API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

# ১. মেইন ল্যান্ডিং পেজ (anondo.bro.bd ভিজিট করলে এটি দেখাবে)
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error: index.html not found in templates folder. Details: {str(e)}"

# ২. চ্যাটবট পেজ (বাটনে ক্লিক করলে এই পেজে আসবে)
@app.route('/chat-page')
def chat_page():
    try:
        return render_template('chat.html')
    except Exception as e:
        return f"Error: chat.html not found. Please rename your old index.html to chat.html. Details: {str(e)}"

# ৩. এআই চ্যাট হ্যান্ডলার (এটি ব্যাকএন্ডে কাজ করবে)
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_data = request.json
        user_message = user_data.get("message")
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are Anondo's AI. Speak in Banglish."},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7
        }

        response = requests.post(URL, headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }, json=data)

        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render-এর জন্য পোর্ট সেটআপ
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
