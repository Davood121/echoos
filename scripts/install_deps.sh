#!/bin/bash
set -e

# EchoOS Dependency Installer
# Installs core system packages, Python deps, and requested languages (Node, Rust, Go)

echo "Updating apt repositories..."
sudo apt update

echo "Installing core packages..."
sudo apt install -y \
  python3 python3-venv python3-pip git build-essential cmake \
  libopenblas-dev libblas-dev liblapack-dev libatlas-base-dev \
  libssl-dev libffi-dev pkg-config curl wget unzip \
  ffmpeg v4l-utils portaudio19-dev python3-pyaudio \
  xdotool xorg-dev libx11-dev libxtst-dev libxrandr-dev \
  libgtk-3-dev \
  nginx \
  sqlite3 \
  docker.io \
  snapd

# --- Node.js (LTS) ---
echo "Installing Node.js (LTS)..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt install -y nodejs
else
    echo "Node.js is already installed."
fi

# --- Rust ---
echo "Installing Rust..."
if ! command -v rustc &> /dev/null; then
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
else
    echo "Rust is already installed."
fi

# --- Go (Golang) ---
echo "Installing Go..."
if ! command -v go &> /dev/null; then
    # Adjust version as needed
    GO_VER="1.21.6"
    wget https://go.dev/dl/go${GO_VER}.linux-amd64.tar.gz
    sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go${GO_VER}.linux-amd64.tar.gz
    rm go${GO_VER}.linux-amd64.tar.gz
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
else
    echo "Go is already installed."
fi

# --- Ollama (AI Runtime) ---
echo "Installing Ollama..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama is already installed."
fi

# --- Python Dependencies ---
echo "Installing Python packages..."
pip3 install --upgrade pip
pip3 install fastapi uvicorn[standard] transformers sentence-transformers chromadb deepface opencv-python-headless pyautogui pywinauto python-dotenv watchdog llm llama-cpp-python coqui-tts sounddevice websockets requests feedparser

echo "Dependency installation complete!"
