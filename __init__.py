import os
import subprocess

# Step 1: Create a virtual environment if it doesn't exist
venv_path = os.path.join(os.getcwd(), '.venv')
if not os.path.exists(venv_path):
    print("Creating virtual environment...")
    subprocess.run(['python', '-m', 'venv', venv_path])

# Step 2: Activate the virtual environment and install requirements
pip_path = os.path.join(venv_path, 'Scripts', 'pip') if os.name == 'nt' else os.path.join(venv_path, 'bin', 'pip')
requirements_file = os.path.join(os.getcwd(), 'requirements.txt')

if os.path.exists(requirements_file):
    print("Installing required modules...")
    subprocess.run([pip_path, 'install', '-r', requirements_file])
    
    # Install Playwright
    print("Installing Playwright...")
    subprocess.run(['playwright', 'install'])
else:
    print("No requirements.txt found. Skipping module installation.")

# Step 3: Create a .env file with a placeholder for API_BASE_URL
env_file = os.path.join(os.getcwd(), '.env')
if not os.path.exists(env_file):
    print("Creating .env file...")
    with open(env_file, 'w') as f:
        f.write("API_BASE_URL=\n")
    print(".env file created. Please set the API_BASE_URL value.")
else:
    print(".env file already exists.")
