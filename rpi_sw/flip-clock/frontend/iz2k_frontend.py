from flask import Flask, send_from_directory, render_template

app = Flask(__name__)
app.run(port=5000, host='0.0.0.0')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

@app.route('/', methods=['GET'])
def main_index():
	return render_template('index.html')

