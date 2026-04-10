from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html') # এটি আপনার হোম পেজ দেখাবে

@app.route('/chat')
def chat():
    return render_template('chat.html') # এটি চ্যাটবট পেজ দেখাবে

if __name__ == "__main__":
    app.run(debug=True)
