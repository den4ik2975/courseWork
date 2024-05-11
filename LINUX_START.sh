#!/bin/bash

# Check if Python 3.10 or higher is installed
python_version=$(python3 --version 2>&1 || true)
if [ -z "$python_version" ]; then
    echo "Python 3.10 or higher is not installed. Installing Python 3.10..."
    # Install Python 3.10 (replace with the appropriate command for your distro)
    sudo apt-get update
    sudo apt-get install -y python3.10
fi

# Check Python version again
python_version=$(python3 --version 2>&1 | awk '{print $2}')
major_version=$(echo "$python_version" | cut -d '.' -f 1)
minor_version=$(echo "$python_version" | cut -d '.' -f 2)

if [ "$major_version" -lt 3 ] || ([ "$major_version" -eq 3 ] && [ "$minor_version" -lt 10 ]); then
    echo "Python 3.10 or higher is required. Please install the correct version and try again."
    exit 1
fi

# Install required packages from requirements.txt
pip3 install -r requirements.txt

# Run src/main.py
python3 main.py
