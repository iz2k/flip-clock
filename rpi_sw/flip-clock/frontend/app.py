# app.py

from flask import Flask, send_from_directory, render_template
from queue import Queue

app = Flask(__name__)
frontendqueue = Queue()
clockcalibration = Queue()