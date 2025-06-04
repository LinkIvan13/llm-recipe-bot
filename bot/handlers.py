import hashlib
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest

from openai_client import ask_gpt, ask_gpt_explanation

router = Router()

# Храним название блюда по ID
dish_registry = {}

def generate_dish_id(dish_title: str) -> str:
    return hashlib.sha1(dish_title.encode()).hexdigest()[:10]  # короткий ID

@router.message(F.text)
async def handle_message(message: Message):
    ingredients = message.text.strip()

    if ingredients.startswith("/"):
        return

    try:
        recipes = ask_gpt(ingredients)

        kb = []
        for r in recipes:
            title = r["title"]
            dish_id = generate_dish_id(title)
            dish_registry[dish_id] = title

            kb.append([
                InlineKeyboardButton(
                    text=f"🧾 Объясни: {title[:30]}",
                    callback_data=f"explain:{dish_id}"
                )
            ])

        response = "\n\n".join(
            f"🍲 <b>{r['title']}</b>\n{r['description']}" for r in recipes
        )

        await message.answer(
            f"📋 <b>Рецепты для:</b> <i>{ingredients}</i>\n\n{response}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=kb),
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(
            f"🍽️ <b>Ошибка GPT</b>\n<code>{str(e)}</code>",
            parse_mode="HTML"
        )


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет!\n"
        "Я помогу сгенерировать рецепты по ингредиентам.\n"
        "Просто пришли список, например:\n"
        "<i>картошка, куриная грудка, морковь</i>",
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("explain:"))
async def explain_dish(callback: CallbackQuery):
    await callback.answer()  # скрыть "загрузка"

    try:
        dish_id = callback.data.split("explain:")[1]
        dish_title = dish_registry.get(dish_id)

        if not dish_title:
            await callback.message.answer("⚠️ Не удалось найти блюдо. Отправьте новый список.")
            return

        explanation = ask_gpt_explanation(dish_title)

        await callback.message.answer(
            f"👨‍🍳 <b>{dish_title}</b>\n\n{explanation}",
            parse_mode="HTML"
        )

    except TelegramBadRequest as e:
        await callback.message.answer(
            f"❌ Ошибка Telegram: <code>{str(e)}</code>",
            parse_mode="HTML"
        )
    except Exception as e:
        await callback.message.answer(
            f"⚠️ Ошибка при генерации пояснения: <code>{str(e)}</code>",
            parse_mode="HTML"
        )


