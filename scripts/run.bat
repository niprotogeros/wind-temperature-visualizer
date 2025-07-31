
@echo off
REM =============================================================================
REM Wind Temperature Visualizer - Windows Launch Script
REM =============================================================================
REM This script activates the virtual environment and launches the Streamlit app
REM Usage: Double-click this file or run from command prompt
REM =============================================================================

echo.
echo ========================================
echo Wind Temperature Visualizer
echo ========================================
echo.

REM Change to project root directory
cd /d "%~dp0.."
if errorlevel 1 (
    echo ERROR: Failed to change to project directory
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv\Scripts\activate.bat (
    echo ERROR: Virtual environment not found!
    echo Please run install.bat first to set up the environment
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if main application file exists
if exist app\main.py (
    set APP_FILE=app\main.py
) else if exist Wind_Temp_visualizer.py (
    set APP_FILE=Wind_Temp_visualizer.py
) else if exist main.py (
    set APP_FILE=main.py
) else (
    echo ERROR: Could not find the main application file
    echo Looking for: app\main.py, Wind_Temp_visualizer.py, or main.py
    pause
    exit /b 1
)

echo.
echo Starting Wind Temperature Visualizer...
echo Application file: %APP_FILE%
echo.
echo The application will open in your default web browser
echo Press Ctrl+C to stop the application
echo.

REM Run the Streamlit application
streamlit run %APP_FILE%

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo Check the error messages above
    pause
)
