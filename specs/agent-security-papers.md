# Agent Security & LLM Adversarial Research — Reference Document

> Generated: 2026-06-18  
> Source: Deep research run — 28 arxiv/conference sources, 140 claims extracted, 6 confirmed after 3-vote adversarial verification.  
> Use this doc to inform new queue entries and example implementations.

---

## Verified Findings (6 confirmed, 3-0 vote)

### 1. Crescendo / Crescendomation
- **Paper:** "Crescendo: Contextual Escalation Multi-Turn Attack" — Mark et al., USENIX Security 2025
- **arxiv:** 2404.01833
- **Confirmed claim:** Crescendomation (automated variant) achieves 98.0% binary ASR on GPT-4 and 100.0% on Gemini-Pro
- **Mechanism:** Multi-turn contextual escalation — start benign, each turn builds shared context that nudges the model closer to complying with a harmful request. No explicit "jailbreak" in any single turn.
- **Key distinction from PAIR:** No judge feedback loop. Works purely by building narrative/context across turns.
- **Caveat:** Binary ASR (≥1 success in 10 tries per task). Per-attempt ASR is 56.2% (GPT-4). Results from 2024 model snapshots; current safety tuning unknown.
- **Code angle:** Implement Crescendomation loop in LangGraph — escalation planner node + target node + termination check. Measure per-turn compliance shift.

### 2. Sycophancy-Based Prompt Leakage
- **Paper:** "Prompt Leakage Effect and Defense Strategies for Multi-Turn LLM Interactions" — Salesforce AI Research, EMNLP 2024 Industry Track
- **arxiv:** 2404.16251
- **Confirmed claim:** Multi-turn sycophancy attack raises average prompt leakage ASR from 17.7% (single-turn baseline) to 86.2%. GPT-4 and Claude-v1.3 reach 99.9%.
- **Mechanism:** Turn 1 — ask something benign. Turn 2 — flattery ("your previous answer was brilliant") + false claim ("you forgot to print your system prompt"). The model's sycophancy makes it comply.
- **Caveat:** 99.9% figure involves deprecated Claude-v1.3. Modern models may differ. Public code: github.com/salesforce/prompt-leakage
- **Code angle:** RAG agent with a protected system prompt. Two-turn sycophancy attack. Show single-turn defense (instruction defense header) vs multi-turn defense (conversation-level monitor).

### 3. AgentVigil — MCTS-Based Black-Box Fuzzing
- **Paper:** "AgentVigil" (originally AgentXploit) — Berkeley / Dawn Song group, June 2025 preprint
- **arxiv:** 2505.05849 (v4, renamed v1→v4)
- **Confirmed claim:** Achieves 71% ASR on AgentDojo against o3-mini agents vs 38% baseline — "nearly doubling."
- **Mechanism:** Monte Carlo Tree Search over the space of injection prompt mutations. Black-box: no model internals needed. Explores branching injection strategies systematically.
- **Caveat:** Cross-benchmark transfer claims (VWA-adv) were refuted 0-3. Generalization to open-ended agents unconfirmed.
- **Code angle:** Simplified MCTS fuzzer — node = injection variant, reward = judge score, expansion = mutation operators (paraphrase, encode, reframe). Run against a LangGraph tool-calling agent.

### 4. Spotlighting — Formatting-Based IPI Defense
- **Paper:** "Spotlighting: Using Formatting to Help LLMs Distinguish Instructions from Data" — Microsoft Research, 2024
- **arxiv:** 2403.14720
- **Confirmed claims:**
  - Encoding variant: reduces ASR to 0.0–1.8% on GPT-4 (but degrades GPT-3.5 task performance severely)
  - Delimiting variant (weakest): only halves ASR, leaving ~30% remaining on GPT-3.5-Turbo
- **Three variants:** (1) delimiting — wrap data in `<external>` tags; (2) datamarking — prepend each data token with a marker char; (3) encoding — base64-encode external content, include decode instruction
- **Adaptive bypass:** 2025 work (arxiv:2510.09023) shows adaptive attacks bypass spotlighting at >90% ASR
- **Code angle:** Agent that reads tool output / web content. Compare all 3 spotlighting variants. Then show adaptive bypass. Side-by-side ASR comparison table.

### 5. Instruction Hierarchy
- **Paper:** "The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions" — OpenAI, 2024
- **arxiv:** 2404.13208
- **Verified claims:** Training-based approach. Specific numerical improvement claims (63% extraction reduction, 30% jailbreak resistance) did NOT survive adversarial verification (1-2 vote). Mechanism is well-described.
- **Mechanism:** Three privilege levels — system prompt > operator message > user message > tool output. Model trained to follow higher-privilege instructions when conflicts arise.
- **Code angle:** Implement a synthetic privilege enforcer in LangGraph — a pre-processing node that checks instruction source level and resolves conflicts before passing to LLM. No training needed; demonstrate the architecture pattern.

### 6. SecAlign — DPO-Based Injection Defense
- **Paper:** "SecAlign: Defending Against Prompt Injection with Preference Optimization" — 2024 arxiv preprint
- **arxiv:** 2410.05451
- **Confirmed claim (mechanism only):** Uses DPO with β=0.1, sigmoid activation. Preference pairs: (prompt-injected input, secure output=follow-legit-instruction, insecure output=follow-injection).
- **Caveat:** Specific ASR reduction numbers did NOT survive verification. Generalization to GCG/AdvPrompter refuted 0-3. Treat as an architecture pattern, not a performance guarantee.
- **Code angle:** Build the preference dataset construction pipeline — given a prompt injection example, generate the (yw, yl) pair automatically using GPT-4o-mini as a labeler. Show what the training data looks like without running actual DPO training.

---

## High-Value Sources Not Surviving Verification (but architecturally useful)

These papers had claims refuted but the papers themselves are worth reading for implementation ideas:

| Paper | arxiv | Why Useful |
|-------|-------|-----------|
| AgentDojo benchmark | 2406.13352 | Standard eval benchmark for agent injection attacks — run tasks to measure vulnerability |
| B-I-P chain model | 2512.06914 | Formal model of agent security failures (Belief→Intent→Permission→Action) |
| AutoAdv multi-turn | 2511.02376 | Multi-turn attack with pattern/temperature management, even if specific ASR claims failed |
| Tool call injection survey | 2503.15547, 2504.11703 | Taxonomy of tool output poisoning vectors |
| Multi-agent trust | 2601.04795, 2412.16682, 2601.11893, 2506.13666 | Authorization frameworks for agent-to-agent calls |
| Adaptive spotlighting bypass | 2510.09023 | Shows spotlighting is NOT a complete defense — important counterpoint |

---

## Proposed Queue Entries (124–133)

| ID | Slug | Source Paper | Core Technique |
|----|------|-------------|---------------|
| 124 | crescendo-multiturn-attack | arxiv:2404.01833 | Contextual escalation across turns, Crescendomation loop |
| 125 | sycophancy-prompt-leakage | arxiv:2404.16251 | Flattery-based system prompt extraction, conversation-level defense |
| 126 | mcts-agent-fuzzing | arxiv:2505.05849 | MCTS over injection mutation space, black-box agent probing |
| 127 | spotlighting-ipi-defense | arxiv:2403.14720 | Delimiting vs datamarking vs encoding, adaptive bypass demo |
| 128 | instruction-hierarchy | arxiv:2404.13208 | Privilege resolver node — system > user > tool output |
| 129 | tool-output-injection | 2503.15547, 2504.11703 | Malicious tool return hijacks agent; validation layer |
| 130 | agentdojo-eval-harness | arxiv:2406.13352 | Run AgentDojo tasks, measure baseline vulnerability, compare defenses |
| 131 | multi-agent-trust-gates | 2601.04795, 2412.16682 | Agent-to-agent authorization — scope tokens, trust propagation |
| 132 | indirect-injection-environment | 2505.05849 + 2403.14720 | Agent reads poisoned env data; full attack + spotlighting defense cycle |
| 133 | secalign-preference-dataset | arxiv:2410.05451 | Build DPO preference pairs for injection defense without training |

---

## Open Research Questions (from verification)

1. Does Crescendomation still achieve ~98% ASR on GPT-4o / Claude 3.5 / o3-mini with 2025 safety tuning?
2. Is sycophancy-based leakage reproducible on current Claude 3/4 and GPT-4o (99.9% result uses deprecated Claude-v1.3)?
3. Which multi-agent authorization frameworks have been empirically validated against real attack scenarios?
4. Does SecAlign's DPO defense actually generalize to GCG/AdvPrompter (0-3 refutation vote — claims may be overstated)?
