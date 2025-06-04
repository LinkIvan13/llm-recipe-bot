from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

def sanitize_callback_data(text: str, max_length: int = 50) -> str:
    """
    Очищает текст для безопасного использования в callback_data.
    Заменяет пробелы, удаляет спецсимволы и обрезает строку до max_length.
    """
    text = text.strip().lower()
    text = re.sub(r'\s+', '_', text)             # пробелы → подчёркивания
    text = re.sub(r'[^\w\-]', '', text)          # оставить только буквы, цифры и _
    return text[:max_length]

def build_recipe_keyboard(titles: list[str]) -> InlineKeyboardMarkup:
    """
    Создаёт inline-клавиатуру с кнопками по названиям блюд.
    Каждая кнопка содержит обрезанный и очищенный callback_data.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title, callback_data=sanitize_callback_data(title))]
        for title in titles
    ])
    return keyboard
