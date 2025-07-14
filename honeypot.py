# honeypot.py
from flask import Flask, request
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Log file to store attack data
log_file = "honeypot_log.csv"

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
        "timestamp": datetime.now(),
        "ip": request.remote_addr,
        "username": request.form.get('username'),
        "password": request.form.get('password'),
        "user_agent": request.headers.get('User-Agent')
    }

    # Log data
    df = pd.DataFrame([data])
    df.to_csv(log_file, mode='a', header=not pd.io.common.file_exists(log_file), index=False)

    return "Invalid credentials!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
