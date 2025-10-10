# app/app.py
from flask import Flask, request
import subprocess

app = Flask(__name__)

# A "safe" endpoint
@app.route('/')
def hello():
    return "Hello, World!"

# An intentionally INSECURE endpoint for your SAST scanner to find later
@app.route('/run')
def run_command():
    command = request.args.get('command')
    # VULNERABILITY: Using shell=True is dangerous!
    subprocess.run(command, shell=True) 
    return f"Executed command: {command}"

if __name__ == '__main__':
    app.run(debug=True) # VULNERABILITY: Running in debug mode is insecure in production.