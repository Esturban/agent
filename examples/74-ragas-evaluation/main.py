from dotenv import load_dotenv

load_dotenv()

from src.workflow import run_evaluation  # noqa: E402


def main() -> None:
    print("Running RAGAS evaluation on 5-row QA dataset...\n")
    result = run_evaluation()
    df = result.to_pandas()
    print(df[["question", "faithfulness", "answer_relevancy"]].to_string(index=False))
    avg_faith = df["faithfulness"].mean()
    avg_rel = df["answer_relevancy"].mean()
    print(f"\nMean faithfulness:     {avg_faith:.3f}")
    print(f"Mean answer_relevancy: {avg_rel:.3f}")


if __name__ == "__main__":
    main()
