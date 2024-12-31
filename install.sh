#!/bin/bash

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y \
    python3 \
    python3-pip \
    vlc \
    git

# Install Python dependencies
pip3 install -r requirements.txt

# Make scripts executable
chmod +x slowtv.sh

# Create example URL file
if [ ! -f urls.txt ]; then
    echo "# Add your YouTube URLs here (one per line)" > urls.txt
    echo "https://www.youtube.com/watch?v=example1" >> urls.txt
    echo "https://www.youtube.com/watch?v=example2" >> urls.txt
fi

echo "Installation complete!"
