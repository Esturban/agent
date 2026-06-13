from datasets import Dataset
from langchain_core.messages import HumanMessage
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness

from src.tools import QA_ROWS, build_rag_chain


def run_evaluation() -> dict:
    retriever, llm = build_rag_chain()
    answers = []
    for row in QA_ROWS:
        docs = retriever.invoke(row["question"])
        ctx = docs[0].page_content if docs else ""
        prompt = f"Context: {ctx}\n\nQuestion: {row['question']}\nAnswer briefly:"
        answer = llm.invoke([HumanMessage(content=prompt)]).content.strip()
        answers.append(answer)

    dataset = Dataset.from_list(
        [
            {
                "question": row["question"],
                "answer": answers[i],
                "contexts": row["contexts"],
                "ground_truth": row["ground_truth"],
            }
            for i, row in enumerate(QA_ROWS)
        ]
    )

    result = evaluate(dataset, metrics=[faithfulness, answer_relevancy])
    return result
