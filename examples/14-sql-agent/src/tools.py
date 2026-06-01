import sqlite3

from langchain_core.tools import tool

DB_PATH = "data/sales.db"


@tool
def list_tables() -> str:
    """List all tables in the database."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    conn.close()
    return ", ".join(r[0] for r in rows) or "No tables found."


@tool
def describe_table(table: str) -> str:
    """Return the column schema of a table."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    conn.close()
    return "\n".join(f"{r[1]} ({r[2]})" for r in rows)


@tool
def run_sql(query: str) -> str:
    """Execute a read-only SQL SELECT query. Returns up to 20 rows."""
    forbidden = {"INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"}
    if any(kw in query.upper() for kw in forbidden):
        return "Only SELECT queries are permitted."
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(query)
    rows = cur.fetchmany(20)
    headers = [d[0] for d in cur.description]
    conn.close()
    lines = [", ".join(headers)] + [", ".join(str(v) for v in row) for row in rows]
    return "\n".join(lines)
