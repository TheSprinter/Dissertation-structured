#!/bin/bash
# Quick start script for Fraud Management Web Application (Linux/Mac)

echo "========================================"
echo "Fraud Management System - Web Application"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "[1/3] Checking dependencies..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
else
    echo "Dependencies already installed."
fi

echo ""
echo "[2/3] Creating output directory..."
mkdir -p output

echo ""
echo "[3/3] Starting Streamlit application..."
echo ""
echo "========================================"
echo "Application will open in your browser"
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

streamlit run app.py
