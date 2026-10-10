@echo off
setlocal enabledelayedexpansion
title Crop Price Intelligence Platform (SIH-36)

echo =====================================================================
echo    SMART INDIA HACKATHON 2026 -- SIH-36: CROP PRICE INTELLIGENCE
echo              Team NODE VI - Gwalior Cluster Platform
echo =====================================================================
echo.

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your System PATH!
    echo Please download and install Python 3.10+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)


:: Check / Create Virtual Environment
if not exist "venv\Scripts\activate.bat" (
    echo [*] Creating virtual environment (venv)...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate Virtual Environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

:: Install / Update Dependencies
echo [*] Checking dependencies...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] Encountered issues installing some packages. Attempting to start...
)

echo.
echo [*] Starting Application Server & Opening Browser...
echo =====================================================================
python run_server.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application terminated with an error.
    pause
)
