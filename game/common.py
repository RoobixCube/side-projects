def break_prompt(text: str):
    user_input = input(text + " (y/N): ")
    return user_input.upper() == 'Y'
