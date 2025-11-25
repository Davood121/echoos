#!/bin/bash
set -e

# EchoOS First Boot Setup
# Downloads models and performs initial checks

MODEL_DIR="/opt/echoos/data/models"
# Example URL - replace with your actual model hosting or local share
MODEL_URL="https://huggingface.co/TheBloke/Phi-3-mini-4k-instruct-GGUF/resolve/main/Phi-3-mini-4k-instruct-q4.gguf?download=true"
MODEL_FILE="$MODEL_DIR/phi-3-mini.gguf"

echo "Running EchoOS First Boot..."

if [ ! -f "$MODEL_FILE" ]; then
    echo "Model not found. Downloading..."
    mkdir -p "$MODEL_DIR"
    curl -L -o "$MODEL_FILE" "$MODEL_URL"
    chown -R echoos:echoos "$MODEL_DIR"
    echo "Model downloaded."
else
    echo "Model already exists."
fi

# Verification
if [ -f "$MODEL_FILE" ]; then
    echo "Verification: Model present."
else
    echo "Verification: Model download failed."
    exit 1
fi

echo "First boot setup complete."
