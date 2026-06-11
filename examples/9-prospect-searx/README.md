# 9-prospect-searx

Prospect research agent upgraded to **SearXNG** — a self-hosted, privacy-focused, multi-engine search backend. Intelligently selects the best engines per query (LinkedIn profiles → Google/Bing; academic → arXiv/PubMed).

**Keys:** `OPENAI_API_KEY` or `OPENROUTER_API_KEY`
**Files:** `data/Connections.csv` (LinkedIn export)
**Services:** SearXNG in Docker
**Colab:** ❌ requires a local Docker daemon

```bash
# Recommended — auto-starts SearXNG, runs agent, cleans up
./examples/9-prospect-searx/run.sh

# Custom date range or input
./examples/9-prospect-searx/run.sh --input data/my_connections.csv --since_date 2025-08-01
```

Output is written to `data/aug/Connections_aug_<timestamp>.csv`.

---

### SearXNG setup (one-time)

**1. Build image:**
```bash
cd ~/Downloads && git clone https://github.com/searxng/searxng.git && cd searxng && make container
```

**2. Create `~/.config/searxng/settings.yml`:**
```yaml
use_default_settings: true
search:
  formats:
    - html
    - json
server:
  secret_key: "change-this"
  limiter: false
```

**3. Verify JSON API works:**
```bash
curl "http://localhost:8888/search?q=test&format=json"
```

If you get `403 Forbidden`, check that `search.formats` includes `json` in your settings file.