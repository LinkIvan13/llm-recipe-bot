from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import BaseModel
from urllib.parse import quote  # ✅ Добавлено

from openai_client import ask_gpt, ask_gpt_explanation
from logger import log_interaction, get_history

app = FastAPI()

# Настройка директорий
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ✅ Добавление фильтра urlencode для Jinja2
templates.env.filters["urlencode"] = lambda u: quote(u)

# Модель запроса для /ask
class Question(BaseModel):
    text: str

# Главная страница — форма ввода ингредиентов
@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Обработка формы — получение рецептов
@app.post("/", response_class=HTMLResponse)
def submit_form(request: Request, ingredients: str = Form(...)):
    recipes = ask_gpt(ingredients)
    log_interaction(ingredients, recipes)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "recipes": recipes,
        "ingredients": ingredients
    })

# Запрос в формате JSON (API-режим)
@app.post("/ask")
def ask(question: Question):
    recipes = ask_gpt(question.text)
    log_interaction(question.text, recipes)
    return {"recipes": recipes}

# История взаимодействий
@app.get("/history", response_class=HTMLResponse)
def view_history(request: Request, from_date: Optional[str] = Query(None), keyword: Optional[str] = Query(None)):
    history = get_history(from_date, keyword)
    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": history,
        "from_date": from_date or "",
        "keyword": keyword or ""
    })

# Пояснение к рецепту
@app.get("/explain", response_class=HTMLResponse)
def explain_recipe(request: Request, title: str = Query(...)):
    print(f"🔍 Получено пояснение для: {title}")
    try:
        explanation = ask_gpt_explanation(title)
    except Exception as e:
        explanation = f"Ошибка при генерации пояснения: {str(e)}"
    return templates.TemplateResponse("explain.html", {
        "request": request,
        "title": title,
        "explanation": explanation
    })
