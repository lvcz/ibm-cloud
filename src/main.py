from flask import Flask, url_for
from flask import request, jsonify
from scrap import step
app = Flask(__name__)
from database import create_new_link_model

@app.route('/')
def index():
    msg = 'usage: \n' \
          ' POST /crawler, form-data: url: <desired_url> \n ' \
          ' POST /crawler/get form-data: url: <crawled_url>'
    return msg


@app.route('/crawler', methods=['POST', 'GET'])
def crawler():
    if request.method == 'POST':
        url = request.form.get('url')
        if url is None:
            return "url not found", 400
        step(url, None)
        return


@app.route('/crawler/get', methods=['POST'])
def get_crawled():
    if request.method == 'POST':
        url = request.form.get('url')
        if url is None:
            return "url not found", 400
        from database import get_my_node, get_all_children
        my_node = get_my_node(url)
        my_children = get_all_children(url)
        child_list = []
        for a in my_children:
            child_list.append(a)
        my_node['children'] = child_list
        return jsonify(my_node)


@app.route('/debug/testdb-connection', methods=['POST'])
def debug_test_connection():
    create_new_link_model('test_url', 'error', None)