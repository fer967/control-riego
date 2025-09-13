import subprocess
import webbrowser
import time

if __name__ == "__main__":
    time.sleep(2)
    webbrowser.open("http://localhost:8000")
    subprocess.run(["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"])

# python start.py
