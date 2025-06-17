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

llm_bot_project/
├── bot/
│ ├── handlers.py # Обработка сообщений и команд
│ ├── keyboards.py # Кнопки (задел)
│ ├── main.py # Запуск Telegram-бота
│ ├── tg_config.py # Загрузка токенов из .env
│ └── init.py
├── main.py # Запуск FastAPI-приложения
├── openai_client.py # Обёртки для OpenAI GPT
├── prompt_builder.py # Формирование prompt'ов
├── templates/ # HTML-шаблоны
│ ├── index.html
│ ├── history.html
│ └── explain.html
├── static/
│ └── style.css # Современные стили
├── logger.py # Логирование и история
├── history.json # История запросов
├── tests/
│ └── test_openai_client.py
├── .env.example # Пример переменных окружения
├── requirements.txt
└── README.md

yaml
Копировать
Редактировать

---

## ⚙️ Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/your-username/llm_bot_project.git
cd llm_bot_project
2. Создайте и активируйте виртуальное окружение
bash
Копировать
Редактировать
python -m venv .venv
source .venv/bin/activate      # для Unix/macOS
.venv\Scripts\activate         # для Windows
3. Установите зависимости
bash
Копировать
Редактировать
pip install -r requirements.txt
4. Настройте переменные окружения
Создайте файл .env в корне и добавьте:

env
Копировать
Редактировать
OPENAI_API_KEY=sk-...
BOT_TOKEN=your_telegram_bot_token
Пример см. в .env.example.

🧪 Запуск FastAPI-приложения
bash
Копировать
Редактировать
uvicorn main:app --reload
Откройте в браузере: http://127.0.0.1:8000

🤖 Запуск Telegram-бота
bash
Копировать
Редактировать
python -m bot.main
Найдите своего бота в Telegram и отправьте ему:

Копировать
Редактировать
яйца, картошка, лук
Бот вернёт рецепты с кнопками для получения объяснений к каждому блюду.

🧾 Пример использования (FastAPI)
Введите ингредиенты на главной странице

Просмотрите рецепты

Нажмите [Подробнее] — чтобы получить пояснение

Перейдите на страницу История, чтобы отфильтровать по дате или ключевым словам

🛠️ Тестирование
bash
Копировать
Редактировать
pytest tests/
