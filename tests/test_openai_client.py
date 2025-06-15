from openai_client import ask_gpt, ask_gpt_explanation

def test_recipe_generation():
    recipes = ask_gpt("яйцо, хлеб, сыр")
    assert isinstance(recipes, list)
    assert all("title" in r and "description" in r for r in recipes)

def test_explanation():
    explanation = ask_gpt_explanation("омлет с сыром")
    assert isinstance(explanation, str)
    assert len(explanation) > 10

if __name__ == "__main__":
    test_recipe_generation()
    test_explanation()
    print("✅ Все тесты успешно прошли.")
