import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from src.workflow import create_workflow

load_dotenv()


def seed_db() -> None:
    Path("data").mkdir(exist_ok=True)
    conn = sqlite3.connect("data/sales.db")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            product TEXT, region TEXT, amount REAL, date TEXT
        );
        INSERT OR IGNORE INTO sales VALUES
            (1,'Widget A','North',1200.00,'2024-01-15'),
            (2,'Widget B','South', 850.50,'2024-01-20'),
            (3,'Widget A','East', 2100.00,'2024-02-05'),
            (4,'Widget C','North', 430.00,'2024-02-18'),
            (5,'Widget B','West', 1750.00,'2024-03-01'),
            (6,'Widget A','South', 990.00,'2024-03-22'),
            (7,'Widget C','East',  610.00,'2024-04-10'),
            (8,'Widget B','North',1340.00,'2024-04-28');
    """)
    conn.commit()
    conn.close()


def main():
    seed_db()
    app = create_workflow()
    print("SQL Agent ready -- type a question or 'quit' to exit.\n")
    while True:
        query = input("You: ").strip()
        if query.lower() in {"quit", "exit", "q"}:
            break
        result = app.invoke({"messages": [HumanMessage(query)]})
        print(f"Agent: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    main()
