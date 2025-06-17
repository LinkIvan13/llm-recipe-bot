import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from prompt_builder import build_recipe_prompt

# Загрузка переменных окружения
load_dotenv()

# Инициализация клиента
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_recipe_line(line: str) -> str:
    """Удаляет номера, точки, дефисы и пробелы из начала строки"""
    return re.sub(r"^[-–•\d\.\)\s]+", "", line).strip()

def ask_gpt(ingredients: str) -> list[dict]:
    """Запрашивает у GPT рецепты по списку ингредиентов"""
    messages = build_recipe_prompt(ingredients)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        raw = response.choices[0].message.content
        data = json.loads(raw)
        return data.get("recipes", [])
    except json.JSONDecodeError:
        return [{"title": "Ошибка", "description": "Модель вернула невалидный JSON."}]
    except Exception as e:
        return [{"title": "Ошибка GPT", "description": str(e)}]

def ask_gpt_explanation(dish: str) -> str:
    """Запрашивает у GPT пояснение, как готовить блюдо, и добавляет КБЖУ"""
    try:
        messages = [
            {
                "role": "system",
                "content": "Ты профессиональный повар. Объясни как приготовить блюдо пошагово."
            },
            {
                "role": "user",
                "content": (
                    f"Расскажи, как приготовить {dish} пошагово. "
                    f"В конце добавь расчёт КБЖУ:\n"
                    f"Калории: ... ккал\nБелки: ... г\nЖиры: ... г\nУглеводы: ... г"
                )
            }
        ]
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка при генерации пояснения: {str(e)}"
