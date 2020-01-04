from flask import Flask, send_from_directory, render_template
import threading
import time
from .app import app
from . import alarm_frontend
from . import spotify_frontend
from . import radio_frontend
from . import clock_frontend

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

@app.route('/', methods=['GET'])
def main_index():
	return render_template('index.html')

def run_app():
	app.run(port=5000, host='0.0.0.0', debug=False)

def iz2k_frontend_init():
	th=threading.Thread(target=run_app).start()
