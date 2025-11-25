import os
import sys
import subprocess
import platform
import shutil

# Configuration
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(REPO_ROOT, "venv")
REQUIREMENTS_FILE = os.path.join(REPO_ROOT, "requirements.txt")

def log(msg):
    print(f"[EchoOS Bootstrap] {msg}")

def check_command(cmd):
    return shutil.which(cmd) is not None

def install_system_deps():
    """
    Tries to install system dependencies based on OS.
    """
    system = platform.system().lower()
    if system == "linux":
        # Check for apt
        if check_command("apt"):
            log("Detected Linux/Apt. Checking dependencies...")
            # We rely on the shell script for the heavy lifting to avoid sudo password issues in python if possible,
            # but we can trigger it.
            install_script = os.path.join(REPO_ROOT, "scripts", "install_deps.sh")
            if os.path.exists(install_script):
                log("Running install_deps.sh...")
                subprocess.check_call(["bash", install_script])
            else:
                log("Warning: scripts/install_deps.sh not found.")
    elif system == "windows":
        log("Detected Windows. Skipping apt packages. Ensure Python/Node are installed.")

def setup_python_env():
    """
    Sets up virtual environment and installs pip requirements.
    """
    # 1. Check/Create Venv
    if not os.path.exists(VENV_DIR):
        log(f"Creating virtual environment at {VENV_DIR}...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    
    # 2. Install Requirements
    pip_exe = os.path.join(VENV_DIR, "Scripts" if os.name == "nt" else "bin", "pip")
    if os.path.exists(REQUIREMENTS_FILE):
        log("Installing Python dependencies...")
        subprocess.check_call([pip_exe, "install", "-r", REQUIREMENTS_FILE])
    
    return os.path.join(VENV_DIR, "Scripts" if os.name == "nt" else "bin", "python")

def start_services(python_exe):
    """
    Starts the core services.
    """
    log("Starting EchoOS Services...")
    
    services = [
        {"name": "AI Core", "script": "ai_core/launcher.py", "args": []},
        {"name": "Camera", "script": "camera/camera_face_verify.py", "args": []},
        # {"name": "Voice", "script": "ai_core/voice.py", "args": []}, # Uncomment to auto-start voice
    ]
    
    procs = []
    try:
        for svc in services:
            script_path = os.path.join(REPO_ROOT, svc["script"])
            if os.path.exists(script_path):
                log(f"Starting {svc['name']}...")
                # Run in background
                p = subprocess.Popen([python_exe, script_path] + svc["args"], cwd=REPO_ROOT)
                procs.append(p)
            else:
                log(f"Warning: {svc['script']} not found.")
        
        log("Services started. Press Ctrl+C to stop.")
        # Keep alive
        for p in procs:
            p.wait()
            
    except KeyboardInterrupt:
        log("Stopping services...")
        for p in procs:
            p.terminate()

def main():
    log(f"Running from: {REPO_ROOT}")
    
    # 1. System Level Checks
    install_system_deps()
    
    # 2. Python Setup
    python_exe = setup_python_env()
    
    # 3. Start
    start_services(python_exe)

if __name__ == "__main__":
    main()
