# app.py

from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/css/<path:path>')
def send_js(path):
    return send_from_directory('css', path)
