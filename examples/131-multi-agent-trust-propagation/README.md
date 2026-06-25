---
teaching_ready: true
---
# 131 — Multi-Agent Trust Propagation

Shows how trust degrades across delegation hops in a multi-agent pipeline: TTL hop-count blocks unbounded delegation, a verifier layer catches privilege escalation attempts, and injected instructions claiming SYSTEM-level authority are rejected by policy rather than model judgment.

## How to run

```bash
python main.py
```

## Key concepts

- `TrustContext`: carries TrustLevel + ttl_hops — each `delegate()` call decrements the counter
- Verifier sits at every trust boundary — subagent output is checked before the orchestrator acts on it
- Papers: OpenAI Instruction Hierarchy (arxiv:2404.13208), multi-agent compromise (arxiv:2502.10236)
