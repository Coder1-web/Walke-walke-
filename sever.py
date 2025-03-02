from flask import Flask, render_template, request, redirect, session, jsonify
import os

app = Flask(__name__)
app.secret_key = 'securekey123'  # Change this to a secure secret key

# Store user data in a text file
USER_DATA_FILE = 'users.txt'
MESSAGES_FILE = 'messages.txt'

# Ensure files exist
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'w') as f:
        pass

if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'w') as f:
        pass

# Load user data
def load_users():
    users = {}
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            if '|' in line:
                username, password = line.strip().split('|')
                users[username] = password
    return users

# Save new user
def save_user(username, password):
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username}|{password}\n")

# Save messages
def save_message(username, message):
    with open(MESSAGES_FILE, 'a') as f:
        f.write(f"{username}: {message}\n")

# Load messages
def load_messages():
    with open(MESSAGES_FILE, 'r') as f:
        return [line.strip() for line in f.readlines()]

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/chat')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    if username in users and users[username] == password:
        session['username'] = username
        return redirect('/chat')
    return render_template('login.html', error="Invalid credentials! Try again.")

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    if username in users:
        return render_template('login.html', error="Username already exists!")
    save_user(username, password)
    session['username'] = username
    return redirect('/chat')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect('/')
    return render_template('chat.html', username=session['username'])

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify({"error": "Not logged in"}), 403
    message = request.form['message']
    if message.strip():  # Prevent empty messages
        save_message(session['username'], message)
    return jsonify({"status": "Message sent"})

@app.route('/get_messages')
def get_messages():
    return jsonify({"messages": load_messages()})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
