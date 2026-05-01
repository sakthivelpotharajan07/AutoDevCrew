import psutil
import subprocess
import time

killed = False
for p in psutil.process_iter(['name', 'cmdline']):
    try:
        cmdline = p.cmdline()
        if cmdline and "python" in cmdline[0].lower() and any("src/main.py" in arg for arg in cmdline) and "api" in cmdline:
            print(f"Killing API server {p.pid}")
            p.kill()
            killed = True
    except Exception:
        pass

if killed:
    print("Restarting API Server in the background...")
    subprocess.Popen(["python", "src/main.py", "api"], start_new_session=True)
    print("API Server restarted successfully.")
else:
    print("API Server not found.")
