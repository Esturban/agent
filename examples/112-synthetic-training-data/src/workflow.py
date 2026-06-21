from pathlib import Path

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from .tools import (
    GeneratedExample,
    LABELS,
    deduplicate_by_embedding,
    embed_examples,
    export_to_jsonl,
    generate_examples_for_label,
    judge_example,
)


def create_workflow(
    n_per_label: int = 6,
    dedup_threshold: float = 0.95,
    skip_judge: bool = False,
    output_path: str = "data/synthetic_train.jsonl",
) -> dict:
    """
    3-stage synthetic data pipeline: generate → deduplicate → judge → export.

    Stage 1 — Generator: GPT-4o produces N examples per label class.
    Stage 2 — Deduplicator: embed all examples, drop pairs with cosine sim > threshold.
    Stage 3 — Judge: second LLM call validates each example is correctly labeled.

    skip_judge=True skips stage 3 (faster, fewer API calls).
    Returns pipeline stats dict.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    print("Stage 1: Generating examples...")
    raw_examples: list[GeneratedExample] = []
    for label in LABELS:
        print(f"  Generating {n_per_label} '{label}' examples...")
        messages = generate_examples_for_label(label, n_per_label, llm)
        for msg in messages:
            raw_examples.append(GeneratedExample(message=msg, label=label))
    print(f"  Generated: {len(raw_examples)} total")

    print("\nStage 2: Embedding + deduplication...")
    texts = [ex.message for ex in raw_examples]
    vecs = embed_examples(texts, embeddings)
    for ex, vec in zip(raw_examples, vecs):
        ex.embedding = vec

    deduped, n_dropped = deduplicate_by_embedding(raw_examples, threshold=dedup_threshold)
    print(f"  Dropped {n_dropped} near-duplicates (threshold={dedup_threshold})")
    print(f"  Remaining: {len(deduped)} examples")

    if not skip_judge:
        print("\nStage 3: Judge validation...")
        judge_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        for i, ex in enumerate(deduped):
            judge_example(ex, judge_llm)
            status = "VALID" if ex.is_valid else "REJECTED"
            print(f"  [{i+1}/{len(deduped)}] {status}: {ex.message[:50]}...")

        n_valid = sum(1 for ex in deduped if ex.is_valid)
        n_rejected = len(deduped) - n_valid
        print(f"  Valid: {n_valid} | Rejected: {n_rejected}")
    else:
        n_valid = len(deduped)
        n_rejected = 0
        print("\nStage 3: Skipped (skip_judge=True)")

    print(f"\nExporting to {output_path}...")
    exported = export_to_jsonl(deduped, output_path)
    print(f"  Exported {exported} examples")

    return {
        "generated": len(raw_examples),
        "after_dedup": len(deduped),
        "n_dropped_dedup": n_dropped,
        "n_valid": n_valid,
        "n_rejected": n_rejected,
        "exported": exported,
        "output_path": output_path,
        "label_breakdown": {
            label: sum(1 for ex in deduped if ex.label == label and ex.is_valid)
            for label in LABELS
        },
    }
