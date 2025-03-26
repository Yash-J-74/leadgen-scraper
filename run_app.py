import subprocess
import os
import signal

# Paths to backend and frontend directories
BACKEND_DIR = os.path.join(os.getcwd(), "backend")
FRONTEND_DIR = os.path.join(os.getcwd(), "frontend")

def run_backend():
    """Run the FastAPI backend."""
    return subprocess.Popen(
        ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=BACKEND_DIR
    )

def run_frontend():
    """Run the Streamlit frontend."""
    return subprocess.Popen(
        ["streamlit", "run", "app.py"],
        cwd=FRONTEND_DIR
    )

if __name__ == "__main__":
    try:
        # Start backend and frontend processes
        backend_process = run_backend()
        frontend_process = run_frontend()

        print("Backend and Frontend are running...")
        print("Backend: http://127.0.0.1:8000")
        print("Frontend: http://127.0.0.1:8501")

        # Wait for processes to complete
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        # Terminate both processes on exit
        backend_process.send_signal(signal.SIGINT)
        frontend_process.send_signal(signal.SIGINT)
        backend_process.wait()
        frontend_process.wait()
