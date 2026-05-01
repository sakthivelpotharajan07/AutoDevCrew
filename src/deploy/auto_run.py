import subprocess
import time
from pyngrok import ngrok
import os
import sys
import psutil

_current_server_process = None

def kill_process_on_port(port):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port and conn.pid:
            try:
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(conn.pid)], capture_output=True)
            except Exception:
                pass
            try:
                proc = psutil.Process(conn.pid)
                proc.terminate()
                proc.wait(timeout=1)
            except Exception:
                pass

def run_and_deploy(project_dir="generated_project", port=8080):
    global _current_server_process
    try:
        print(f"Cleaning up old processes on port {port} and tunnels...")
        if _current_server_process is not None:
            try:
                pid = _current_server_process.pid
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True)
            except Exception:
                pass
            _current_server_process = None
            
        kill_process_on_port(port)
        try:
            ngrok.kill() # Terminate previous pyngrok tunnels
        except Exception:
            pass
        
        # Force kill any remaining ngrok processes
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and 'ngrok' in proc.info['name'].lower():
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Step 1: install requirements
        req_path = os.path.join(project_dir, "requirements.txt")
        if os.path.exists(req_path):
            print(f"Installing requirements from {req_path}...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--no-input", "--disable-pip-version-check", "-r", "requirements.txt"], cwd=project_dir, check=True)
        else:
            print("No requirements.txt found. Skipping installation.")

        # Step 2: detect backend type and start server
        possible_paths = [
            os.path.join(project_dir, "main.py"),
            os.path.join(project_dir, "app.py"),
            os.path.join(project_dir, "src", "main.py"),
            os.path.join(project_dir, "src", "app.py"),
            os.path.join(project_dir, "api", "main.py"),
            os.path.join(project_dir, "api", "app.py"),
            os.path.join(project_dir, "app", "main.py"),
            os.path.join(project_dir, "app", "app.py")
        ]
        
        main_file = None
        for path in possible_paths:
            if os.path.exists(path):
                main_file = path
                break
                
        if not main_file:
            raise RuntimeError("Could not detect backend type. Neither `main.py` nor `app.py` found in project root or common subdirectories.")

        with open(main_file, "r", encoding="utf-8") as f:
            content = f.read()

        is_flask = "Flask" in content
        is_fastapi = "FastAPI" in content
        
        rel_path = os.path.relpath(main_file, project_dir)
        module_name = rel_path.replace(os.sep, ".").replace(".py", "")

        if is_flask:
            print(f"Detected Flask backend. Starting Flask on port {port}...")
            env = os.environ.copy()
            env["FLASK_APP"] = rel_path
            env["FLASK_RUN_PORT"] = str(port)
            env["FLASK_RUN_HOST"] = "0.0.0.0"
            if "PYTHONPATH" in env:
                env["PYTHONPATH"] = f"{project_dir}{os.pathsep}{env['PYTHONPATH']}"
            else:
                env["PYTHONPATH"] = project_dir
                
            _current_server_process = subprocess.Popen(
                [sys.executable, "-m", "flask", "run"],
                cwd=project_dir,
                env=env
            )
        else:
            print(f"Detected FastAPI backend. Starting Uvicorn on port {port}...")
            _current_server_process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", f"{module_name}:app", "--host", "0.0.0.0", "--port", str(port)],
                cwd=project_dir
            )

        # Wait for server to start
        time.sleep(5)
        
        # Check if the server crashed immediately
        if _current_server_process.poll() is not None:
             raise RuntimeError(f"Server crashed immediately with exit code {_current_server_process.returncode}. Check generated requirements or code syntax.")

        # Step 3: start ngrok targeting the correct port
        print(f"Creating ngrok tunnel on port {port}...")
        tunnel = ngrok.connect(port)
        
        return tunnel.public_url

    except Exception as e:
        print(f"Error during run and deploy: {e}")
        return f"Error: {e}"
