from flask import Flask, url_for
from flask import request, jsonify
from scrap import step
app = Flask(__name__)


@app.route('/')
def index():
    return 'index'


@app.route('/crawler', methods=['POST', 'GET'])
def crawler():
    if request.method == 'POST':
        url = request.form.get('url')
        if url is None:
            return "url not found", 400
        step(url, None)
        return
