@echo off
REM Quick start script for Fraud Management Web Application

echo ========================================
echo Fraud Management System - Web Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Dependencies already installed.
)

echo.
echo [2/3] Creating output directory...
if not exist "output" mkdir output

echo.
echo [3/3] Starting Streamlit application...
echo.
echo ========================================
echo Application will open in your browser
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python -m streamlit run app.py

pause
