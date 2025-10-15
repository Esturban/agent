# Prospect Agent with SearXNG

This example demonstrates an intelligent prospect research agent that uses **SearXNG** for privacy-focused, multi-engine search. The agent researches prospects and generates personalized outreach messages.

## Quick Start (Recommended)

The easiest way to run this agent is using the included automation script:

```bash
# From the repo root
./examples/9-prospect-searx/run.sh

# With custom date range
./examples/9-prospect-searx/run.sh --since_date 2025-08-01 --to_date 2025-08-31

# With custom input file
./examples/9-prospect-searx/run.sh --input data/my_connections.csv
```

The script automatically:
- Starts SearXNG in Docker
- Waits for it to be ready
- Runs the agent
- Stops and cleans up the container

## Prerequisites

### 1. Build SearXNG Docker Image

Follow the [SearXNG Docker build instructions](https://docs.searxng.org/admin/installation-docker.html):

```bash
# Clone and build SearXNG
cd ~/Downloads
git clone https://github.com/searxng/searxng.git
cd searxng
make container
```
Note: for more installation instructions, see: https://docs.searxng.org/dev/quickstart.html 

Here are the complete instructions for building from source: https://docs.searxng.org/admin/installation-docker.html

### 2. Configure SearXNG Settings

Create `~/.config/searxng/settings.yml`:

```yaml
use_default_settings: true

search:
  formats:
    - html
    - json

server:
  secret_key: "ultrasecretkey12345"  # Change this!
  limiter: false
```

This enables JSON API access for the agent.

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# SearXNG (optional, defaults to http://localhost:8888)
SEARXNG_HOST=http://localhost:8888
SEARCH_WAIT_SECONDS=1.0

# API Keys (required)
OPENROUTER_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Debug mode (optional)
SEARXNG_DEBUG=false
```

### SearXNG Settings Location

The agent uses `~/.config/searxng/settings.yml` which is mounted into the Docker container.

## Usage

### Option 1: Automated Script (Recommended)

```bash
# Default: processes recent connections
./examples/9-prospect-searx/run.sh

# Custom date range
./examples/9-prospect-searx/run.sh --since_date 2025-08-01 --to_date 2025-08-31

# Custom input file
./examples/9-prospect-searx/run.sh --input data/my_connections.csv

# All options
./examples/9-prospect-searx/run.sh \
  --input data/Connections.csv \
  --since_date 2025-08-01 \
  --to_date 2025-08-28
```

### Option 2: Manual Docker + Python

If you prefer manual control:

```bash
# Start SearXNG container
docker run -d --name searxng -p 8888:8080 \
  -v ~/.config/searxng/settings.yml:/etc/searxng/settings.yml:ro \
  localhost/searxng/searxng:latest

# Wait for it to be ready
curl "http://localhost:8888/search?q=test&format=json"

# Run the agent
python examples/9-prospect-searx/main.py --input data/Connections.csv

# Stop container
docker stop searxng && docker rm searxng
```

Output will be written to `data/aug/Connections_aug_<timestamp>.csv`.

## How It Works

### Intelligent Engine Selection

The researcher agent automatically selects the best search engines for each query:

- **LinkedIn/Profiles** → `google,bing`
- **Recent News** → `reuters,bing`
- **Tech/Code** → `github,gitlab`
- **Academic** → `arxiv,pubmed`
- **General Business** → `google,bing,duckduckgo`

### Available SearXNG Engines

Common engines you can use (configured in your SearXNG instance):
- `google`, `bing`, `duckduckgo`
- `brave`, `reuters`
- `github`, `gitlab`
- `arxiv`, `pubmed`
- And many more (see SearXNG docs)

### Output Format

CSV output includes:
- `generated_message`: Personalized outreach message (≤300 chars)
- `confidence`: AI confidence score (0-1)
- `source_summary`: Top 2-3 URLs separated by `; `

If no recent information found: `No recent information found for this prospect.`

## Troubleshooting

### Script Fails to Start

If `run.sh` fails, check:

1. **Docker image exists:**
   ```bash
   docker images | grep searxng
   ```
   If missing, build it from the SearXNG source directory.

2. **Settings file exists:**
   ```bash
   cat ~/.config/searxng/settings.yml
   ```
   Should contain the JSON format configuration.

3. **Port 8888 is free:**
   ```bash
   lsof -i :8888
   ```
   Kill any process using the port.

### 403 Forbidden Error

If you see `403 Forbidden` when testing manually:

```bash
curl "http://localhost:8888/search?q=test&format=json"
```

Your `~/.config/searxng/settings.yml` is missing or incorrect. Ensure it has:

```yaml
use_default_settings: true

search:
  formats:
    - html
    - json

server:
  secret_key: "ultrasecretkey12345"
  limiter: false
```

**Important:** The key setting is `search.formats` must include `json`.

### Enable Debug Mode

Get detailed diagnostic information:

```bash
export SEARXNG_DEBUG=true
./examples/9-prospect-searx/run.sh
```

This will show:
- Exact URLs being called
- Response status codes  
- Search engines selected
- Number of results returned

### Docker Container Won't Start

Check the logs:

```bash
docker logs searxng-prospect-agent
```

Common issues:
- Settings file has syntax errors (validate YAML)
- Port 8080 is already in use inside container
- Read-only volume mount failing

### Manual Testing

Test SearXNG without the agent:

```bash
# Start container manually
docker run -d --name searxng-test -p 8888:8080 \
  -v ~/.config/searxng/settings.yml:/etc/searxng/settings.yml:ro \
  localhost/searxng/searxng:latest

# Wait 5 seconds, then test
sleep 5
curl "http://localhost:8888/search?q=test&format=json"

# Should return JSON with search results
# Clean up
docker stop searxng-test && docker rm searxng-test
```

## Inspiration

Based on [LangGraph Research Agent](https://www.pinecone.io/learn/langgraph-research-agent/)