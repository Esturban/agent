#!/bin/bash
# Prospect Agent with SearXNG - Automated Runner
# This script starts SearXNG in Docker, runs the agent, and cleans up

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
SEARXNG_CONTAINER_NAME="searxng-prospect-agent"
SEARXNG_PORT="8888"
SEARXNG_SETTINGS="${HOME}/.config/searxng/settings.yml"
SEARXNG_IMAGE="localhost/searxng/searxng:latest"

# Parse command line arguments (pass through to Python)
PYTHON_ARGS="$@"

echo -e "${BLUE}=== SearXNG Prospect Agent Runner ===${NC}"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${BLUE}Cleaning up...${NC}"
    docker stop ${SEARXNG_CONTAINER_NAME} 2>/dev/null || true
    docker rm ${SEARXNG_CONTAINER_NAME} 2>/dev/null || true
    echo -e "${GREEN}✓ Cleanup complete${NC}"
}

# Register cleanup function
trap cleanup EXIT INT TERM

# Check if SearXNG settings exist
if [ ! -f "${SEARXNG_SETTINGS}" ]; then
    echo -e "${RED}✗ SearXNG settings not found at ${SEARXNG_SETTINGS}${NC}"
    echo "  Please ensure ~/.config/searxng/settings.yml exists"
    exit 1
fi

# Check if Docker image exists
if ! docker image inspect ${SEARXNG_IMAGE} >/dev/null 2>&1; then
    echo -e "${RED}✗ SearXNG Docker image not found: ${SEARXNG_IMAGE}${NC}"
    echo "  Please build the image first from the SearXNG source directory:"
    echo "  cd ~/Desktop/eva/03_development/_dev/ext/searxng"
    echo "  docker build -t localhost/searxng/searxng:latest ."
    exit 1
fi

# Stop any existing container
docker stop ${SEARXNG_CONTAINER_NAME} 2>/dev/null || true
docker rm ${SEARXNG_CONTAINER_NAME} 2>/dev/null || true

# Start SearXNG container
echo -e "${BLUE}Starting SearXNG container...${NC}"
docker run -d \
    --name ${SEARXNG_CONTAINER_NAME} \
    -p ${SEARXNG_PORT}:8080 \
    -v ${SEARXNG_SETTINGS}:/etc/searxng/settings.yml:ro \
    ${SEARXNG_IMAGE} >/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ SearXNG container started${NC}"
else
    echo -e "${RED}✗ Failed to start SearXNG container${NC}"
    exit 1
fi

# Wait for SearXNG to be ready
echo -e "${BLUE}Waiting for SearXNG to be ready...${NC}"
for i in {1..30}; do
    if curl -s "http://localhost:${SEARXNG_PORT}/search?q=test&format=json" >/dev/null 2>&1; then
        echo -e "${GREEN}✓ SearXNG is ready${NC}"
        break
    fi
    
    if [ $i -eq 30 ]; then
        echo -e "${RED}✗ SearXNG failed to start within 30 seconds${NC}"
        docker logs ${SEARXNG_CONTAINER_NAME}
        exit 1
    fi
    
    sleep 1
done

# Run the Python agent
echo -e "${BLUE}Running prospect agent...${NC}"
cd "$(dirname "$0")/../.."  # Navigate to repo root

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Run with default or custom arguments
if [ -z "$PYTHON_ARGS" ]; then
    # Default: recent connections
    python examples/9-prospect-searx/main.py \
        --input data/Connections.csv \
        --since_date 2025-08-01
else
    # Custom arguments
    python examples/9-prospect-searx/main.py ${PYTHON_ARGS}
fi

AGENT_EXIT_CODE=$?

if [ $AGENT_EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}✓ Agent completed successfully${NC}"
else
    echo -e "\n${RED}✗ Agent failed with exit code ${AGENT_EXIT_CODE}${NC}"
fi

# Cleanup happens automatically via trap
exit $AGENT_EXIT_CODE

