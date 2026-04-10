@app.route('/')
def home():
    return render_template('index.html') # এইটাই আপনার হাব পেজ দেখাবে

@app.route('/chat')
def chat():
    return render_template('chat.html') # আপনার আগের চ্যাট ইন্টারফেস
