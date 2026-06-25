# 145 — LoRA Architecture Ablation

Sweeps four LoRA configs (rank 4–32, different target modules) and prints a comparison table of trainable parameter % vs. training loss. Shows how rank and target module choice affect parameter efficiency.

**Run:** `python main.py` — works on CPU for small models; Colab T4 recommended for speed
