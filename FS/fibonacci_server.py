from flask import Flask, request, jsonify
import socket
app = Flask(__name__)

def register_with_authoritative_server(hostname, ip, as_ip, as_port):
    message = (
        "TYPE=A\n"
        f"NAME={hostname}\n"
        f"VALUE={ip}\n"
        "TTL=10\n"
    ).encode('utf-8')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.sendto(message, (as_ip, int(as_port)))
        data, server = sock.recvfrom(1024)
        print(f"Received response: {data.decode('utf-8')}")

    finally:
        sock.close()

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@app.route('/')
def hello_world():
    return 'Hello World! This is fibonacci server!'

@app.route('/register' ,methods=['PUT'])
def register():
    data = request.json
    hostname = data.get("hostname")
    ip = data.get("ip")
    as_ip = data.get("as_ip")
    as_port = data.get("as_port")

    if not hostname or not ip or not as_ip or not as_port:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        register_with_authoritative_server(hostname,ip,as_ip,as_port)
        return jsonify({"status": "registered"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')

    try:
        x = int(number)
    except ValueError:
        return "Invalid input, X must be an integer", 400

    result = fibonacci(x)
    return jsonify({"fibonacci": result}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)