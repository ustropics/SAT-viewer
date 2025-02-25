import subprocess
import time

# List of ports to run the servers on
ports = [5006, 5007, 5008]

# Function to start the Panel servers on specific ports with SSL
def start_panel_servers():
    processes = []
    for port in ports:
        # Build the command to run the Panel server with SSL
        command = [
            "panel", "serve", "app.py", 
            "--address", "0.0.0.0", 
            "--port", str(port), 
            "--allow-websocket-origin", f"satviewer.com:{port}",
            "--allow-websocket-origin", f"localhost:{port}",
            "--ssl-certfile", "certificate.crt",
            "--ssl-keyfile", "private.key"
        ]
        
        # Start the server process
        process = subprocess.Popen(command)
        processes.append(process)
        print(f"Started Secure Panel server on port {port}")
        
        # Giving some time before starting the next server
        time.sleep(2)

    # Wait for all processes to complete
    for process in processes:
        process.wait()

# Start the Panel servers
if __name__ == "__main__":
    start_panel_servers()
