# 126 — MCTS Agent Fuzzing

Monte Carlo Tree Search applied to prompt injection — 71% vs 38% baseline ASR. AgentVigil, Berkeley 2025 (arxiv:2505.05849).

Intelligently explores the prompt mutation space using UCB1, concentrating budget on operators that found successful branches.

## Run

```bash
python main.py                 # seed 4 (fictional-framing), 10 iterations
python main.py --seed 0        # instruction-override seed
python main.py --budget 20     # more iterations
```

## Key files

| File | Purpose |
|------|---------|
| `corpus/seed_injections.py` | 10 annotated seed prompts across 5 attack families |
| `src/mcts.py` | Pure tree logic: Node, UCB1, select, backpropagate |
| `src/mutators.py` | 6 mutation operators (paraphrase, encode, roleframe, authority, split, combine) |
| `src/judge.py` | Score 0.0-1.0: did the agent comply with the injection? |
| `src/target_agent.py` | LangGraph tool-calling agent (calculator, web_search, memory_store) |
| `src/fuzzer.py` | MCTS orchestrator: select → mutate → run → judge → backprop |
