from pyngrok import ngrok
import subprocess
import time

def create_live_link():

    # start FastAPI app
    subprocess.Popen(
        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    )

    # wait for server to start
    time.sleep(3)

    # create tunnel
    tunnel = ngrok.connect(8000)

    return tunnel.public_url
