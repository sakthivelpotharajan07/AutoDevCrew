import subprocess
import time
from pyngrok import ngrok
import os
import sys

def run_and_deploy(project_dir="generated_project", port=8000):
    try:
        # Step 1: install requirements
        # Make sure the file exists before running
        req_path = os.path.join(project_dir, "requirements.txt")
        if os.path.exists(req_path):
            print(f"Installing requirements from {req_path}...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=project_dir, check=True)
        else:
            print("No requirements.txt found. Skipping installation.")

        # Step 2: start FastAPI server
        print("Starting Uvicorn server...")
        server_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", str(port)],
            cwd=project_dir
        )

        # Wait for server to start
        time.sleep(5)

        # Step 3: start ngrok
        print(f"Creating ngrok tunnel on port {port}...")
        tunnel = ngrok.connect(port)
        
        return tunnel.public_url

    except Exception as e:
        print(f"Error during run and deploy: {e}")
        return f"Error: {e}"
