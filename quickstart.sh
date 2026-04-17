#!/bin/bash
# Maha Verify AI - Quick Start Script for macOS/Linux

echo "🔧 Maha Verify AI - Setup"
echo

# Check Python version
if ! python3 --version &> /dev/null; then
    echo "❌ Python3 not found"
    exit 1
fi

echo "✓ Python detected"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Create directories
mkdir -p uploads

# Setup .env file
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "⚠️  Created .env file - Please configure API keys!"
    fi
fi

echo "✓ Setup complete!"
echo
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python quickstart.py"
