#!/bin/bash
# Quick debug test - processes just 1 prospect with full debug output

cd "$(dirname "$0")/../.."

export SEARXNG_DEBUG=true

# Start SearXNG if not running
if ! docker ps | grep -q searxng; then
    echo "Starting SearXNG..."
    docker run -d --name searxng -p 8888:8080 \
        -v ~/.config/searxng/settings.yml:/etc/searxng/settings.yml:ro \
        localhost/searxng/searxng:latest
    sleep 5
fi

source .venv/bin/activate 2>/dev/null || true

# Run with just 1 prospect for testing
python examples/9-prospect-searx/main.py \
    --input data/Connections.csv \
    --since_date 2025-08-05 \
    --to_date 2025-08-05

echo ""
echo "=== Debug test complete ==="

