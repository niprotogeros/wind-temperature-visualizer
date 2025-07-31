
@echo off
REM =============================================================================
REM Wind Temperature Visualizer - Windows Installation Script
REM =============================================================================
REM This script creates a virtual environment and installs all dependencies
REM Usage: Double-click this file or run from command prompt
REM =============================================================================

echo.
echo ========================================
echo Wind Temperature Visualizer Installer
echo ========================================
echo.

REM Change to project root directory
cd /d "%~dp0.."
if errorlevel 1 (
    echo ERROR: Failed to change to project directory
    pause
    exit /b 1
)

echo Current directory: %CD%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Remove existing virtual environment if it exists
if exist venv (
    echo Removing existing virtual environment...
    rmdir /s /q venv
    if errorlevel 1 (
        echo WARNING: Could not remove existing venv directory
    )
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure you have the venv module installed
    pause
    exit /b 1
)

echo Virtual environment created successfully!
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)

REM Install dependencies
echo.
echo Installing dependencies from requirements.txt...
if not exist requirements.txt (
    echo ERROR: requirements.txt not found in project root
    echo Make sure you're running this script from the correct location
    pause
    exit /b 1
)

pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Check the error messages above and try again
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo You can now run the application using run.bat
echo or by running: streamlit run app/main.py
echo.
pause
