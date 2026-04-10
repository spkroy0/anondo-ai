from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html') # আপনার সেই হোম পেজ

@app.route('/chat')
def chat():
    return render_template('chat.html') # আপনার চ্যাটবট পেজ

if __name__ == "__main__":
    app.run()
