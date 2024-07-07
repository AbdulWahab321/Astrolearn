import webbrowser
import os
import sys
import threading
import socket
import signal
import subprocess  # Use subprocess to manage the Flask process

port = 5000
# Global variable to store the Flask process
flask_process = None

def run_app():
    global flask_process
    try:
        # Start the Flask app process
        flask_process = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "main.py"), f'127.0.0.1:{port}'])
    except Exception as e:
        print(f"Failed to start Flask app: {e}")
        sys.exit(1)  # Exit the script with an error code


# Start Flask app in a separate thread
threading.Thread(target=run_app).start()

# Create the webview window
webbrowser.open(f"http://127.0.0.1:{port}")


