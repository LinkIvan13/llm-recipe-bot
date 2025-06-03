from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from openai_client import ask_gpt, ask_gpt_explanation

router = Router()


@router.message(F.text)
async def handle_message(message: Message):
    ingredients = message.text.strip()

    # Игнорируем команды вида /start, /help и т.д.
    if ingredients.startswith("/"):
        return

    try:
        recipes = ask_gpt(ingredients)
        if not recipes:
            raise ValueError("Ответ пустой или не содержит рецептов.")

        text = f"📋 <b>Рецепты для:</b> <i>{ingredients}</i>\n\n"
        keyboard = InlineKeyboardBuilder()

        for r in recipes:
            text += f"🍲 <b>{r['title']}</b>\n{r['description']}\n\n"
            keyboard.row(
                InlineKeyboardButton(
                    text=f"👨‍🍳 Объясни: {r['title']}",
                    callback_data=f"explain:{r['title']}"
                )
            )

        await message.answer(text, reply_markup=keyboard.as_markup(), parse_mode="HTML")

    except Exception as e:
        await message.answer(
            f"🍽️ <b>Ошибка</b>\nМодель вернула невалидный JSON.\n\n<code>{str(e)}</code>",
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
    dish = callback.data.split(":", 1)[1]
    await callback.answer()  # чтобы убрать "загрузка" у кнопки

    try:
        explanation = ask_gpt_explanation(dish)
        await callback.message.answer(f"👨‍🍳 <b>{dish}</b>\n\n{explanation}", parse_mode="HTML")
    except Exception as e:
        await callback.message.answer(
            f"⚠️ Ошибка при получении пояснения: <code>{str(e)}</code>",
            parse_mode="HTML"
        )

