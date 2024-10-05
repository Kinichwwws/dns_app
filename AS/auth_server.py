from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)


@app.route('/home')
def AS_home():
    return "This is AS home page"


@app.route('/', methods=['GET', 'POST'])
def AS():
    file = 'address_map.json'
    if not os.path.exists(file):
        os.system(r'touch address_map.json')
        file = 'address_map.json'

    ## US ask ip address of a hostname
    if request.method == 'GET':
        key = request.args.get('name')
        with open(file, 'r') as json_file:
            data = json.load(json_file)
            if key not in data:
                return jsonify({"error": "hostname not found"}), 404
            else:
                address = data.get(key)
                return jsonify({"address": address}), 200

    ## FS register information in AS
    elif request.method == 'POST':
        data_get = request.form
        host_name = data_get['name']
        ip_address = data_get['address']
        dict = {}
        dict[host_name] = ip_address
        with open(file, 'w') as json_file:
            json.dump(dict, json_file)
        return jsonify({"success registered": True}), 201


app.run(host='0.0.0.0',
        port=53533,
        debug=True)