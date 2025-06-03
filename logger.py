import json
from datetime import datetime
from typing import Any
from typing import Optional

HISTORY_FILE = "history.json"

def log_interaction(question: str, response: Any) -> None:
    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "response": response
    }

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append(entry)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def get_history(from_date: Optional[str] = None, keyword: Optional[str] = None) -> list:
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    result = []

    for entry in history:
        if from_date and entry["timestamp"] < from_date:
            continue
        if keyword and keyword.lower() not in entry["question"].lower():
            continue
        result.append(entry)

    return result
