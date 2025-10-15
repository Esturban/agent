# SearXNG Prospect Agent - Quick Start

## One-Time Setup

### 1. Build SearXNG Docker Image

```bash
git clone https://github.com/searxng/searxng.git searxng
cd searxng
make container
docker run -d --name searxng -p 8888:8080 \
        -v ~/.config/searxng/settings.yml:/etc/searxng/settings.yml:ro \
        localhost/searxng/searxng:latest

```

### 2. Configure SearXNG

Create `~/.config/searxng/settings.yml`:

```yaml
use_default_settings: true

search:
  formats:
    - html
    - json

server:
  secret_key: "ultrasecretkey12345"  # Change to a random string
  limiter: false
```

### 3. Configure Agent

Create `.env` in repo root:

```env
OPENROUTER_API_KEY=your_openrouter_key
OPENAI_API_KEY=your_openai_key
SEARXNG_HOST=http://localhost:8888  # Optional, this is default
SEARCH_WAIT_SECONDS=1.0  # Optional, this is default
```

## Daily Usage

### Run with Default Settings

Processes connections from the last few months:

```bash
./examples/9-prospect-searx/run.sh
```

### Run with Date Range

```bash
./examples/9-prospect-searx/run.sh --since_date 2025-08-01 --to_date 2025-08-31
```

### Run with Custom Input

```bash
./examples/9-prospect-searx/run.sh --input data/my_connections.csv
```

### Debug Mode

```bash
export SEARXNG_DEBUG=true
./examples/9-prospect-searx/run.sh
```

## Output

Results are saved to: `data/aug/Connections_aug_<timestamp>.csv`

Each row includes:
- All original CSV columns
- `generated_message`: Personalized outreach (≤300 chars)
- `confidence`: AI confidence score (0-1)
- `source_summary`: Top 2-3 source URLs

## What the Script Does

1. **Starts SearXNG** in Docker container
2. **Waits for readiness** (up to 30 seconds)
3. **Runs the agent** with your parameters
4. **Cleans up** the container automatically

Even if the agent fails or you Ctrl+C, cleanup happens automatically!

## Troubleshooting

### "Docker image not found"

```bash
cd ~/Downloads/searxng
docker build -t localhost/searxng/searxng:latest .
```

### "Settings file not found"

```bash
mkdir -p ~/.config/searxng
cat > ~/.config/searxng/settings.yml << 'EOF'
use_default_settings: true

search:
  formats:
    - html
    - json

server:
  secret_key: "ultrasecretkey12345"
  limiter: false
EOF
```

### "Port 8888 already in use"

```bash
# Find what's using it
lsof -i :8888

# If it's a SearXNG container:
docker stop searxng-prospect-agent && docker rm searxng-prospect-agent
```

### Script hangs at "Waiting for SearXNG"

Check the container logs:

```bash
docker logs searxng-prospect-agent
```

Most common cause: Invalid YAML in settings file.

## Architecture

```
┌─────────────────────────────────────────────┐
│  run.sh (Orchestrator)                      │
│                                             │
│  1. Start SearXNG Docker container          │
│  2. Wait for health check                   │
│  3. Run Python agent                        │
│  4. Cleanup container (even on failure)     │
└─────────────────────────────────────────────┘
           │                        │
           ▼                        ▼
    ┌──────────────┐        ┌─────────────────┐
    │   SearXNG    │◄───────│  Python Agent   │
    │   (Docker)   │        │                 │
    │              │        │  • Researcher   │
    │ Multi-engine │        │  • Copywriter   │
    │ search API   │        │  • CSV output   │
    └──────────────┘        └─────────────────┘
```

## Engine Selection

The agent intelligently selects search engines based on query type:

- **LinkedIn/Profiles** → google, bing
- **Recent News** → reuters, bing  
- **Tech/Code** → github, gitlab
- **Academic** → arxiv, pubmed
- **General Business** → google, bing, duckduckgo

This happens automatically via the LLM researcher.

