from flask import Flask, redirect, request
from flask_sockets import Sockets
import random
import requests
from flask_reverse_proxy import ReverseProxied
from concurrent.futures import ThreadPoolExecutor
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
sockets = Sockets(app)

bokeh_servers = [
    "https://satviewer.com:5006",
    "https://satviewer.com:5007",
    "https://satviewer.com:5008"
]

app.wsgi_app = ReverseProxied(app.wsgi_app)

# Function to check a server's availability
def check_server(server):
    try:
        response = requests.get(f"{server}/app", timeout=2, verify=False)  # Ignore SSL verification for self-signed certs
        if response.status_code == 200:
            return server
    except requests.exceptions.RequestException:
        return None

# Function to check server availability asynchronously
def check_server_availability():
    with ThreadPoolExecutor() as executor:
        available_servers = list(filter(None, executor.map(check_server, bokeh_servers)))
    return available_servers

@app.route('/')
def index():
    available_servers = check_server_availability()

    if not available_servers:
        return "No Bokeh servers are available.", 503

    chosen_server = random.choice(available_servers)
    return redirect(f"{chosen_server}/app")

@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    available_servers = check_server_availability()
    if not available_servers:
        return "No Bokeh servers are available.", 503

    chosen_server = random.choice(available_servers)

    url = f"{chosen_server}/{path}"
    response = requests.request(
        method=request.method,
        url=url,
        headers=request.headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        verify=False  # Ignore SSL verification for self-signed certs
    )

    return (response.content, response.status_code, response.headers.items())

# WebSocket route for proxying WebSocket to Panel server
@sockets.route('/ws')
def websocket(ws):
    available_servers = check_server_availability()
    if not available_servers:
        ws.close()
        return

    chosen_server = random.choice(available_servers)

    bokeh_ws_url = f"wss://{chosen_server.split('//')[1]}/ws"

    with websocket.WebSocketClient(bokeh_ws_url) as client_ws:
        while not ws.closed:
            message = ws.receive()
            if message:
                client_ws.send(message)
            response = client_ws.receive()
            if response:
                ws.send(response)

# Start the Flask app with SSL
if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 443), app, handler_class=WebSocketHandler, keyfile="private.key", certfile="certificate.crt")
    http_server.serve_forever()
