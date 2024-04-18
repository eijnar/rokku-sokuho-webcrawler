#!/bin/bash

# Determine the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Setup Python virtual environment
python3 -m venv "$SCRIPT_DIR/venv"
source "$SCRIPT_DIR/.venv/bin/activate"
pip install -r "$SCRIPT_DIR/requirements.txt"

# Enable linger for the user
loginctl enable-linger $(whoami)

# Update service and timer files with correct paths and user
sed -i "s|%h|$HOME|g" "$SCRIPT_DIR/rokku-sokuho.service"
sed -i "s|%u|$(whoami)|g" "$SCRIPT_DIR/rokku-sokuho.service"
sed -i "s|%h|$HOME|g" "$SCRIPT_DIR/rokku-sokuho-gunicorn.service"
sed -i "s|%u|$(whoami)|g" "$SCRIPT_DIR/rokku-sokuho-gunicorn.service"

# Install systemd service and timer files
mkdir -p "$HOME/.config/systemd/user/"
cp "$SCRIPT_DIR/rokku-sokuho.service" "$HOME/.config/systemd/user/"
cp "$SCRIPT_DIR/rokku-sokuho.timer" "$HOME/.config/systemd/user/"
cp "$SCRIPT_DIR/rokku-sokuho-frontend.service" "$HOME/.config/systemd/user/"

# Reload systemd daemon to recognize new service and timer
systemctl --user daemon-reload

# Enable and start the services and timer
systemctl --user enable rokku-sokuho.timer
systemctl --user start rokku-sokuho.timer
systemctl --user enable rokku-sokuho-frontend.service
systemctl --user start rokku-sokuho-frontend.service

echo "Installation completed successfully."
