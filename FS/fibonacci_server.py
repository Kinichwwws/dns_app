import requests
from flask import Flask, request, jsonify
import socket
app = Flask(__name__)

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@app.route('/')
def hello_world():
    return 'Hello World! This is fibonacci server!'


@app.route('/register', methods=['PUT'])
def register():
    # 从请求体中获取 JSON 数据
    data = request.json
    hostname = data['hostname']
    ip = data['ip']
    as_ip = data['as_ip']
    as_port = data['as_port']

    # Register with Authoritative Server
    dns_registration = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    as_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    as_socket.sendto(dns_registration.encode(), (as_ip, int(as_port)))

    return "Registration successful", 201


@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')

    try:
        x = int(number)
        result=fibonacci(x)
        return jsonify({"fibonacci": result}), 200
    except ValueError:
        return "Invalid input, X must be an integer", 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)