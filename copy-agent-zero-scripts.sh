#!/bin/bash

# Script to copy files from Agent Zero Docker container
# Usage: ./copy-agent-zero-scripts.sh <container_name_or_id>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <container_name_or_id>"
    echo "Example: $0 agent-zero-container"
    exit 1
fi

CONTAINER=$1
DEST_DIR="./apps/survey-automation/scripts"

echo "Copying scripts from Agent Zero container: $CONTAINER"

# Copy the three main scripts
echo "Copying browser_use_script.py..."
docker cp "$CONTAINER:/root/browser_use_script.py" "$DEST_DIR/browser_use_script.py"

echo "Copying skyvern_script.py..."
docker cp "$CONTAINER:/root/skyvern_script.py" "$DEST_DIR/skyvern_script.py"

echo "Copying combined_skyvern_script.py..."
docker cp "$CONTAINER:/root/combined_skyvern_script.py" "$DEST_DIR/combined_skyvern_script.py"

echo "Scripts copied successfully!"
echo "Main script to use: $DEST_DIR/combined_skyvern_script.py"

# Make the script executable
chmod +x "$0"
