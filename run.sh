#!/bin/bash

env_example="env.example"
env_file=".env"
venv_dir="venv"

# Check if .env file already exists
if [ -f "$env_file" ]; then
    echo ".env file already exists. Please delete or rename it and try again. Aborting."
    exit 1
fi

# Check if .env.example file exists
if [ ! -f "$env_example" ]; then
    echo ".env.example file not found. Aborting."
    exit 1
fi

# Copy contents from .env.example to .env
cp "$env_example" "$env_file"
echo "Created .env file from $env_example"

# Create and activate virtual environment
python -m venv "$venv_dir"
source "$venv_dir/bin/activate"

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Run the app
python app.py
