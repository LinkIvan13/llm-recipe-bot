from fastapi import FastAPI, Request, Form, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.concurrency import run_in_threadpool
from typing import Optional
from pydantic import BaseModel
from urllib.parse import quote
import logging

from openai_client import ask_gpt, ask_gpt_explanation
from logger import log_interaction, get_history

app = FastAPI()

# Настройка директорий
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.filters["urlencode"] = lambda u: quote(u)


# Модель для API-запроса
class Question(BaseModel):
    text: str


# Главная страница с формой
@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


# Обработка формы — генерация рецептов
@app.post("/", response_class=HTMLResponse)
async def submit_form(request: Request, ingredients: str = Form(...)) -> HTMLResponse:
    if not ingredients.strip():
        raise HTTPException(status_code=400, detail="Поле ингредиентов не должно быть пустым")

    try:
        recipes = await run_in_threadpool(ask_gpt, ingredients)
        await run_in_threadpool(log_interaction, ingredients, recipes)
    except Exception as e:
        logging.exception("Ошибка при обработке запроса рецепта")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Ошибка генерации рецептов: {str(e)}"
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "recipes": recipes,
        "ingredients": ingredients
    })


# API-доступ к рецептам
@app.post("/ask")
async def ask(question: Question) -> dict:
    try:
        recipes = await run_in_threadpool(ask_gpt, question.text)
        await run_in_threadpool(log_interaction, question.text, recipes)
        return {"recipes": recipes}
    except Exception as e:
        logging.exception("Ошибка при API-запросе рецепта")
        return {"error": str(e)}


# Просмотр истории
@app.get("/history", response_class=HTMLResponse)
async def view_history(request: Request, from_date: Optional[str] = Query(None),
                       keyword: Optional[str] = Query(None)) -> HTMLResponse:
    try:
        history = await run_in_threadpool(get_history, from_date, keyword)
    except Exception as e:
        logging.exception("Ошибка при получении истории")
        history = []
    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": history,
        "from_date": from_date or "",
        "keyword": keyword or ""
    })


# Объяснение рецепта
@app.get("/explain", response_class=HTMLResponse)
async def explain_recipe(request: Request, title: str = Query(...)) -> HTMLResponse:
    try:
        explanation = await run_in_threadpool(ask_gpt_explanation, title)
    except Exception as e:
        logging.exception("Ошибка при генерации пояснения")
        explanation = f"Ошибка при генерации пояснения: {str(e)}"
    return templates.TemplateResponse("explain.html", {
        "request": request,
        "title": title,
        "explanation": explanation
    })
