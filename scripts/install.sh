
#!/usr/bin/env bash
# =============================================================================
# Wind Temperature Visualizer - Unix Installation Script (macOS/Linux)
# =============================================================================
# This script creates a virtual environment and installs all dependencies
# Usage: ./install.sh
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
echo "Wind Temperature Visualizer Installer"
echo "========================================"
echo

# Change to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo -e "${BLUE}Current directory: $(pwd)${NC}"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}ERROR: Python is not installed or not in PATH${NC}"
        echo "Please install Python 3.7+ from your package manager or https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo -e "${GREEN}Python found:${NC}"
$PYTHON_CMD --version
echo

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if [[ $(echo "$PYTHON_VERSION < 3.7" | bc -l) -eq 1 ]]; then
    echo -e "${RED}ERROR: Python 3.7+ is required, but found Python $PYTHON_VERSION${NC}"
    exit 1
fi

# Remove existing virtual environment if it exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}Removing existing virtual environment...${NC}"
    rm -rf venv
fi

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
$PYTHON_CMD -m venv venv

if [ ! -d "venv" ]; then
    echo -e "${RED}ERROR: Failed to create virtual environment${NC}"
    echo "Make sure you have the venv module installed"
    exit 1
fi

echo -e "${GREEN}Virtual environment created successfully!${NC}"
echo

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip || echo -e "${YELLOW}WARNING: Failed to upgrade pip, continuing anyway...${NC}"

# Install dependencies
echo
echo -e "${BLUE}Installing dependencies from requirements.txt...${NC}"
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}ERROR: requirements.txt not found in project root${NC}"
    echo "Make sure you're running this script from the correct location"
    exit 1
fi

pip install -r requirements.txt

echo
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Installation completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo
echo "You can now run the application using:"
echo -e "${BLUE}  ./scripts/run.sh${NC}"
echo "or by running:"
echo -e "${BLUE}  source venv/bin/activate && streamlit run app/main.py${NC}"
echo
