#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Litestar Habit Tracker - Local Development Server ===${NC}\n"

# Check if .env exists
if [[ ! -f ".env" ]]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo "Please create a .env file based on .env.example !!!"
    exit 1
fi

# Activate virtual environment if it exists
if [[ -d ".venv" ]]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source .venv/bin/activate
else
    echo -e "${YELLOW}No virtual environment found. Creating one...${NC}"
    python3.11 -m venv .venv
    source .venv/bin/activate
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install --upgrade pip
    pip install poetry
    poetry install
fi

# Start PostgreSQL via docker compose
echo -e "${YELLOW}Starting PostgreSQL database...${NC}"
# Check if db_dev container is already running
if docker ps --filter "name=db_dev" --filter "status=running" | grep -q db_dev; then
    echo -e "${GREEN}Database container (db_dev) is already running${NC}"
else
    # Check if container exists but is stopped
    if docker ps -a --filter "name=db_dev" | grep -q db_dev; then
        echo -e "${YELLOW}Starting existing db_dev container...${NC}"
        docker start db_dev
    else
        echo -e "${YELLOW}Creating and starting new db_dev container...${NC}"
        docker compose --profile dev up -d
    fi
    echo -e "${GREEN}Database container started${NC}"
fi
    
# Wait for PostgreSQL to be ready
echo -e "${YELLOW}Waiting for PostgreSQL to be ready...${NC}"
sleep 3

# Load environment variables from .env
echo -e "${YELLOW}Loading environment variables from .env...${NC}"
set -a
source .env
set +a

# Alembic migrations
echo -e "${YELLOW}Running Alembic migrations...${NC}"

poetry run alembic upgrade head

# Check if port 8000 is available
if command -v lsof &> /dev/null; then
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}Warning: Port 8000 is already in use${NC}"
        PID=$(lsof -t -i :8000)
        echo "Process ID: $PID"
        echo ""
        read -p "Kill the process? (y/n) " choice
        if [[ "$choice" == "y" ]]; then
            kill -9 "$PID"
            echo "Process killed. Starting server..."
        else
            echo -e "${RED}Error: Port 8000 is still in use${NC}"
            exit 1
        fi
    fi
else
    echo -e "${YELLOW}lsof not available, skipping port check${NC}"
fi

# Run the app 
echo -e "${GREEN}Starting Litestar development server...${NC}"

poetry run python src/app.py
