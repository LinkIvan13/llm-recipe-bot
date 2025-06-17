import json
import logging
from datetime import datetime
from typing import Any, Optional

# Настройка логов в файл
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

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

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        logging.info("Сохранена история запроса: %s", question)
    except Exception as e:
        logging.exception("Ошибка при записи истории: %s", e)

def get_history(from_date: Optional[str] = None, keyword: Optional[str] = None) -> list:
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logging.warning("История пуста или повреждена")
        return []

    result = []

    for entry in history:
        timestamp = entry.get("timestamp", "")
        question = entry.get("question", "")

        # Фильтрация по дате (если корректный формат)
        if from_date:
            try:
                if timestamp < from_date:
                    continue
            except Exception as e:
                logging.warning("Неверный формат даты фильтра: %s", from_date)
                continue

        # Фильтрация по ключевому слову
        if keyword and keyword.lower() not in question.lower():
            continue

        result.append(entry)

    return result
