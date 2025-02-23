import subprocess

def launch_dev_server():
    """
    Launches the Panel development server with proper WebSocket handling.
    """
    cmd = [
        "panel", "serve", "app.py",
        "--dev",  # Enable hot-reloading
        "--address", "0.0.0.0",
        "--port", "5006",
        "--allow-websocket-origin=localhost:5006"
    ]
    
    print("Starting Panel development server on http://localhost:5006...")
    subprocess.run(cmd)

if __name__ == "__main__":
    launch_dev_server()