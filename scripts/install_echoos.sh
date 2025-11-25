#!/bin/bash
set -e

# EchoOS Main Installer

INSTALL_DIR="/opt/echoos"
REPO_DIR="$(pwd)"

echo "Starting EchoOS Installation..."

# 1. Install Dependencies
if [ -f "./scripts/install_deps.sh" ]; then
    chmod +x ./scripts/install_deps.sh
    ./scripts/install_deps.sh
else
    echo "Warning: install_deps.sh not found. Skipping dependency check."
fi

# 2. Create User
echo "Creating echoos user..."
if ! id "echoos" &>/dev/null; then
    sudo useradd -m -s /bin/bash echoos
    sudo usermod -aG sudo,video,docker echoos
    echo "User 'echoos' created."
else
    echo "User 'echoos' already exists."
fi

# 3. Copy Files
echo "Installing files to $INSTALL_DIR..."
sudo mkdir -p $INSTALL_DIR
sudo cp -r ./* $INSTALL_DIR/
sudo chown -R echoos:echoos $INSTALL_DIR

# 4. Install Systemd Services
echo "Installing systemd services..."
sudo cp services/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable echoos-ai.service
sudo systemctl enable echoos-camera.service
# sudo systemctl enable echoos-ui.service # Enable when UI is ready

echo "Installation Complete!"
echo "Run 'sudo systemctl start echoos-ai' to start the AI core."
