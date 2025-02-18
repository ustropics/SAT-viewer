import asyncio
import subprocess

# Define a range of ports for multiple Panel instances
ports = [5006, 5007, 5008]  # Add more ports as needed
public_ip = "satviewer.com"  # Use your domain

async def launch_panel_server(port):
    """Launches a Panel server on the specified port."""
    cmd = [
        "panel", "serve", "app.py",
        "--address", "0.0.0.0",
        "--port", str(port),
        "--allow-websocket-origin", f"{public_ip}",
        "--allow-websocket-origin", f"{public_ip}:80"
    ]
    process = await asyncio.create_subprocess_exec(*cmd)
    return process

async def main():
    """Launches multiple Panel servers asynchronously."""
    tasks = [launch_panel_server(port) for port in ports]
    processes = await asyncio.gather(*tasks, return_exceptions=True)

    # Keep the event loop running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping Panel servers...")
        for process in processes:
            process.terminate()
        await asyncio.gather(*(p.wait() for p in processes))

if __name__ == "__main__":
    asyncio.run(main())
