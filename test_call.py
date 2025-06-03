from openai_client import ask_gpt

recipes = ask_gpt("молоко, яйца, мука")
for r in recipes:
    print(r)
