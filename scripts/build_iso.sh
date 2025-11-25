#!/bin/bash
set -e

# EchoOS ISO Builder (Wrapper for live-build)
# Usage: ./build_iso.sh [output_dir]

BUILD_DIR="${1:-$HOME/echoos-iso-build}"
REPO_DIR="$(pwd)"

echo "Preparing build directory at $BUILD_DIR..."
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

# Check for live-build
if ! command -v lb &> /dev/null; then
    echo "Error: live-build not found. Please run: sudo apt install live-build"
    exit 1
fi

echo "Configuring live-build..."
lb config --distribution jammy --architectures amd64 --debian-installer live --archive-areas "main universe restricted multiverse"

# Create config directories
mkdir -p config/package-lists
mkdir -p config/hooks/normal
mkdir -p config/includes.chroot/opt/echoos

# 1. Package List
cat <<EOF > config/package-lists/echoos.list.chroot
python3 python3-venv python3-pip git build-essential cmake libssl-dev libffi-dev ffmpeg 
python3-opencv sqlite3 nginx docker.io xdotool xorg open-vm-tools
nodejs npm rustc cargo golang-go
EOF

# 2. Copy Repo Content
echo "Copying repository to build context..."
cp -r "$REPO_DIR/"* config/includes.chroot/opt/echoos/

# 3. Hooks
cat <<EOF > config/hooks/normal/01-setup-echoos.sh
#!/bin/bash
set -e
# Create user
useradd -m -s /bin/bash echoos
usermod -aG sudo,video,docker echoos
echo "echoos:echoos" | chpasswd
# Fix permissions
chown -R echoos:echoos /opt/echoos
# Enable services
systemctl enable echoos-ai.service || true
systemctl enable echoos-camera.service || true
EOF
chmod +x config/hooks/normal/01-setup-echoos.sh

# 4. Build
echo "Starting build (this may take a while)..."
sudo lb build

echo "Build complete! ISO should be in $BUILD_DIR"
