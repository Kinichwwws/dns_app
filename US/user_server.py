from flask import Flask, request, jsonify
import requests, socket

app = Flask(__name__)

def query_authoritative_server(as_ip, as_port, hostname):
    # queries for authoritative server for IP address of the given hostname.
    message = f"TYPE=A\nNAME={hostname}\n"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    try:
        sock.sendto(message.encode(), (as_ip, as_port))
        response, _ = sock.recvfrom(1024)

        lines = response.decode().splitlines()
        for line in lines:
            if line.startswith("TYPE="):
                return line.split('=')[1]
    except socket.timeout:
        print("Socket timeout")
        return None
    finally:
        sock.close()

    return None

@app.route('/')
def hello_world():
    return 'Hello World! This is User Server!'

@app.route("/fibonacci", methods=['GET'])
def get_fibonacci():
    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify({"status": "error", "message": "Missing parameters"}), 400

    # Query AS for IP address of Fibonacci Server
    fs_if = query_authoritative_server(as_ip, as_port, hostname)

    if not fs_if:
        return jsonify({"status": "error", "message": "Invalid hostname"}), 400

    #request the Fibonacci number from the Fibonacci

    try:
        response = requests.get(f"http://{fs_if}:{fs_port}" + f"/fibonacci?number={number}", timeout=2)
        if response.status_code == 200:
            return jsonify({"status": "ok", "fibonacci": response.json().get("fibonacci")}), 200
        else:
            return jsonify({"status": "error", "message": response.text}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)



