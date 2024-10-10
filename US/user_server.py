# US/user_server.py
from flask import Flask, request
import requests
import socket

app = Flask(__name__)

@app.route('/fibonacci')
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Bad Request: Missing parameters", 400

    # Query AS to get IP address for the hostname
    dns_query = f"TYPE=A\nNAME={hostname}\n"
    as_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    as_socket.sendto(dns_query.encode(), (as_ip, int(as_port)))
    response, _ = as_socket.recvfrom(1024)
    response = response.decode().split('\n')
    ip_address = response[2].split('=')[1]

    # Query FS to get Fibonacci number
    fs_url = f"http://{ip_address}:{fs_port}/fibonacci?number={number}"
    response = requests.get(fs_url)

    if response.status_code == 200:
        return response.text, 200
    else:
        return "Error fetching Fibonacci number", response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)