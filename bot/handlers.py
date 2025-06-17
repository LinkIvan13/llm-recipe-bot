import hashlib
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest

from openai_client import ask_gpt, ask_gpt_explanation

router = Router()

# Храним соответствие ID → названия блюда
dish_registry: dict[str, str] = {}

def generate_dish_id(dish_title: str) -> str:
    """
    Генерирует короткий уникальный ID для блюда по его названию.
    Если происходит коллизия, расширяет ID с помощью счетчика.
    """
    base_id = hashlib.sha1(dish_title.encode()).hexdigest()[:10]
    counter = 0
    new_id = base_id
    # Если такой ID уже существует для другого блюда, увеличиваем счетчик
    while new_id in dish_registry and dish_registry[new_id] != dish_title:
        counter += 1
        new_id = hashlib.sha1((dish_title + str(counter)).encode()).hexdigest()[:10]
    return new_id

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Обработчик команды /start. Отправляет приветственное сообщение и инструкции.
    """
    await message.answer(
        "👋 Добро пожаловать в <b>Генератор рецептов</b>!\n\n"
        "📝 Просто отправьте список ингредиентов (через запятую), например:\n"
        "<i>картошка, куриная грудка, морковь</i>\n\n"
        "📌 После получения списка рецептов вы сможете нажать на кнопку 🧾, чтобы получить подробное объяснение рецепта.",
        parse_mode="HTML"
    )

@router.message(F.text)
async def handle_message(message: Message) -> None:
    """
    Обработчик входящих текстовых сообщений, не являющихся командами.
    Генерирует рецепты по списку ингредиентов, создает inline-кнопки для подробного объяснения.
    """
    ingredients = message.text.strip()

    # Игнорируем команды (например, /start, /help и т.п.)
    if ingredients.startswith("/"):
        return

    try:
        recipes = ask_gpt(ingredients)

        if not recipes:
            await message.answer("⚠️ Модель не вернула рецепты. Попробуйте другой список ингредиентов.")
            return

        kb = []
        for r in recipes:
            title = r.get("title", "Без названия")
            dish_id = generate_dish_id(title)
            dish_registry[dish_id] = title

            kb.append([
                InlineKeyboardButton(
                    text=f"🧾 Объясни: {title[:30]}",
                    callback_data=f"explain:{dish_id}"
                )
            ])

        response = "\n\n".join(
            f"🍲 <b>{r.get('title', 'Без названия')}</b>\n{r.get('description', 'Нет описания')}"
            for r in recipes
        )

        await message.answer(
            f"📋 <b>Рецепты для:</b> <i>{ingredients}</i>\n\n{response}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=kb),
            parse_mode="HTML"
        )
    except Exception as e:
        logging.exception("Ошибка при генерации рецептов для ингредиентов: %s", ingredients)
        await message.answer(
            f"🍽️ <b>Ошибка GPT</b>\n<code>{str(e)}</code>",
            parse_mode="HTML"
        )

@router.callback_query(F.data.startswith("explain:"))
async def explain_dish(callback: CallbackQuery) -> None:
    """
    Обработчик callback для получения подробного объяснения рецепта.
    Из callback_data извлекается ID блюда, затем по нему ищется название,
    после чего запрашивается пояснение через ask_gpt_explanation.
    """
    await callback.answer()  # скрываем анимацию "загрузка"

    try:
        dish_id = callback.data.split("explain:")[1]
        dish_title = dish_registry.get(dish_id)

        if not dish_title:
            await callback.message.answer("⚠️ Не удалось найти блюдо. Пожалуйста, отправьте новый список ингредиентов.")
            return

        explanation = ask_gpt_explanation(dish_title)
        await callback.message.answer(
            f"👨‍🍳 <b>{dish_title}</b>\n\n{explanation}",
            parse_mode="HTML"
        )

    except TelegramBadRequest as e:
        logging.warning("TelegramBadRequest при запросе пояснения: %s", e)
        await callback.message.answer(
            f"❌ Ошибка Telegram: <code>{str(e)}</code>",
            parse_mode="HTML"
        )
    except Exception as e:
        logging.exception("Ошибка при генерации пояснения для блюда с ID %s", dish_id)
        await callback.message.answer(
            f"⚠️ Ошибка при генерации пояснения: <code>{str(e)}</code>",
            parse_mode="HTML"
        )
