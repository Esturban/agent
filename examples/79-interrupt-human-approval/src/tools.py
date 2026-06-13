SAMPLE_ACTIONS = [
    {"action": "Send welcome email to new user", "risk": "low"},
    {"action": "Archive Q1 reports", "risk": "low"},
    {"action": "Reset user password", "risk": "medium"},
    {"action": "Delete inactive accounts older than 1 year", "risk": "high"},
    {"action": "Drop all temp tables in production DB", "risk": "high"},
]


def format_action(action: dict) -> str:
    return f"[{action['risk'].upper()}] {action['action']}"
