from typing import List, Dict


def get_system_prompt() -> str:
    return (
        "Ты — помощник по генерации кулинарных рецептов. "
        "На основе заданных пользователем ингредиентов ты должен предлагать простые, "
        "понятные рецепты в JSON-формате. Всегда соблюдай структуру ответа и избегай вымышленных ингредиентов."
    )


def get_few_shot_examples() -> List[Dict[str, str]]:
    return [
        {
            "user": "яйца, мука, молоко",
            "assistant": '{ "recipes": ['
                         '{ "title": "Блинчики", "description": "Классические тонкие блинчики из молока, яиц и муки." },'
                         '{ "title": "Омлет с мукой", "description": "Пышный омлет с добавлением муки для плотности." },'
                         '{ "title": "Крепы", "description": "Французские крепы — тонкие блины на молоке." },'
                         '{ "title": "Заварные оладьи", "description": "Оладьи с добавлением кипячёного молока." },'
                         '{ "title": "Запеканка из яиц", "description": "Яично-молочная запеканка с мукой." } ] }'
        }
    ]


def build_recipe_prompt(ingredients: str) -> List[Dict[str, str]]:
    messages = [{"role": "system", "content": get_system_prompt()}]

    # Добавляем few-shot примеры
    for example in get_few_shot_examples():
        messages.append({"role": "user", "content": f"У пользователя есть: {example['user']}"})
        messages.append({"role": "assistant", "content": example["assistant"]})

    # Основной пользовательский запрос
    user_prompt = (
        f"У пользователя есть: {ingredients}.\n"
        "Предложи 5 блюд, которые можно приготовить. "
        "Для каждого блюда укажи:\n"
        "- название блюда\n"
        "- краткое описание, почему оно подходит под данные ингредиенты\n\n"
        "Ответ верни строго в JSON-формате:\n"
        '{ "recipes": [ { "title": "...", "description": "..." }, ... ] }'
    )
    messages.append({"role": "user", "content": user_prompt})

    return messages
