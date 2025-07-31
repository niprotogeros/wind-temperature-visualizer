
#!/usr/bin/env bash
# =============================================================================
# Wind Temperature Visualizer - Unix Launch Script (macOS/Linux)
# =============================================================================
# This script activates the virtual environment and launches the Streamlit app
# Usage: ./run.sh
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo
echo "========================================"
echo "Wind Temperature Visualizer"
echo "========================================"
echo

# Change to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo -e "${RED}ERROR: Virtual environment not found!${NC}"
    echo "Please run ./scripts/install.sh first to set up the environment"
    echo
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Find the main application file
if [ -f "app/main.py" ]; then
    APP_FILE="app/main.py"
elif [ -f "Wind_Temp_visualizer.py" ]; then
    APP_FILE="Wind_Temp_visualizer.py"
elif [ -f "main.py" ]; then
    APP_FILE="main.py"
else
    echo -e "${RED}ERROR: Could not find the main application file${NC}"
    echo "Looking for: app/main.py, Wind_Temp_visualizer.py, or main.py"
    exit 1
fi

echo
echo -e "${GREEN}Starting Wind Temperature Visualizer...${NC}"
echo -e "${BLUE}Application file: $APP_FILE${NC}"
echo
echo "The application will open in your default web browser"
echo -e "${YELLOW}Press Ctrl+C to stop the application${NC}"
echo

# Run the Streamlit application
streamlit run "$APP_FILE"
