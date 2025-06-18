# 🍽️ AI Recipe Generator — Генератор рецептов с ИИ

Интеллектуальный помощник, который генерирует рецепты по списку ингредиентов с помощью GPT-4. Поддерживает веб-интерфейс (FastAPI) и Telegram-бота с inline-кнопками.

---

## 🚀 Возможности

- 🧠 Генерация до 5 рецептов по введённым ингредиентам  
- 🧾 Пояснение к любому рецепту по запросу  
- 💬 Telegram-бот с кнопками «Объясни»  
- 🌐 HTML-интерфейс (FastAPI) с историей и фильтрацией  
- 🧠 Интеграция с OpenAI GPT API  
- 📜 Локальное логирование и история взаимодействий (history.json)  

---

## 📁 Структура проекта

'''
llm_bot_project/
├── bot/
│   ├── handlers.py          # Обработка сообщений и команд
│   ├── keyboards.py         # Кнопки (задел)
│   ├── main.py              # Запуск Telegram-бота
│   ├── tg_config.py         # Загрузка токенов из .env
│   └── __init__.py
├── main.py                  # Запуск FastAPI-приложения
├── openai_client.py         # Обёртки для OpenAI GPT
├── prompt_builder.py        # Формирование prompt'ов
├── templates/               # HTML-шаблоны
│   ├── index.html
│   ├── history.html
│   └── explain.html
├── static/
│   └── style.css            # Современные стили
├── logger.py                # Логирование и история
├── history.json             # История запросов
├── tests/
│   └── test_openai_client.py
├── .env.example             # Пример переменных окружения
├── requirements.txt
└── README.md
'''

---

## ⚙️ Установка и запуск

### 1. Клонируйте репозиторий

***
git clone https://github.com/your-username/llm_bot_project.git
cd llm_bot_project
***

### 2. Создайте и активируйте виртуальное окружение

***
python -m venv .venv
source .venv/bin/activate      # для Unix/macOS
.venv\Scripts\activate         # для Windows
***

### 3. Установите зависимости

***
pip install -r requirements.txt
***

### 4. Настройте переменные окружения

Создайте файл .env в корне и добавьте:

***
OPENAI_API_KEY=sk-...
BOT_TOKEN=your_telegram_bot_token
***

Пример см. в .env.example.

---

## 🧪 Запуск FastAPI-приложения

***
uvicorn main:app --reload
***

Откройте в браузере: http://127.0.0.1:8000

---

## 🤖 Запуск Telegram-бота

***
python -m bot.main
***

Найдите своего бота в Telegram и отправьте ему, например:

***
яйца, картошка, лук
***

Бот вернёт рецепты с кнопками для получения объяснений к каждому блюду.

---

## 🧾 Пример использования (FastAPI)

1. Введите ингредиенты на главной странице  
2. Просмотрите сгенерированные рецепты  
3. Нажмите «Подробнее» — чтобы получить пояснение  
4. Перейдите на страницу История, чтобы отфильтровать по дате или ключевым словам  

---

## 🛠️ Тестирование

***
pytest tests/
***

---

## 📺 Видео-обзор

🔗 [Смотреть демо на Google.Диске](https://drive.google.com/file/d/1-CEPiQ_3sv4QZWvdo4mwOPCrbwlksU0z/view?usp=sharing)