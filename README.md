# 🍽️ AI Recipe Generator

Интеллектуальный помощник, который генерирует рецепты по списку ингредиентов с использованием GPT-4. Интерфейсы: FastAPI (веб) и Telegram-бот.

---

## 🚀 Возможности

- Ввод ингредиентов и генерация 5 рецептов с описанием
- Объяснение выбранного рецепта по запросу
- Поддержка Telegram-бота с кнопками
- HTML-форма на FastAPI
- Интеграция с OpenAI GPT API
- Локальное хранение истории запросов

---

## 📁 Структура проекта

llm_bot_project/
├── .env.example # Пример файла окружения
├── main.py # FastAPI-приложение
├── telegram_bot/
│ ├── init.py
│ ├── bot.py # Инициализация бота
│ ├── handlers.py # Обработка сообщений и команд
│ └── keyboards.py # Inline-кнопки
├── openai_client.py # Логика работы с GPT API
├── prompt_builder.py # Конструирование промптов
├── templates/
│ └── form.html # HTML-форма FastAPI
├── static/
│ └── style.css # Стили для формы
├── README.md
└── requirements.txt


---

## ⚙️ Установка

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/ваш-профиль/llm_bot_project.git
cd llm_bot_project

2. Создайте и активируйте виртуальное окружение

python -m venv .venv
source .venv/bin/activate  # для Unix/macOS
.venv\Scripts\activate     # для Windows

3. Установите зависимости

pip install -r requirements.txt
4. Настройте переменные окружения
Создайте файл .env в корне и вставьте свои ключи:


OPENAI_API_KEY=sk-...
TELEGRAM_BOT_TOKEN=your_bot_token
Пример см. в .env.example.

💡 Запуск FastAPI-приложения

uvicorn main:app --reload
Перейдите в браузере: http://127.0.0.1:8000

💬 Запуск Telegram-бота

python telegram_bot/bot.py
Затем найдите вашего бота в Telegram по имени и отправьте ему список ингредиентов, например:
курица, рис, чеснок
Вы получите список рецептов, каждый с возможностью запроса пояснения.