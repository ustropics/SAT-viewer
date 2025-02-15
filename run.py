import subprocess

ports = [5006, 5007, 5008]
public_ip = "73.42.46.217"  # Or use "localhost"

processes = []
for port in ports:
    cmd = [
        "panel", "serve", "app.py",
        "--address", "0.0.0.0",
        "--port", str(port),
        "--allow-websocket-origin", f"{public_ip}:80"
    ]
    process = subprocess.Popen(cmd)
    processes.append(process)

try:
    for process in processes:
        process.wait()
except KeyboardInterrupt:
    print("Stopping Panel servers...")
    for process in processes:
        process.terminate()
