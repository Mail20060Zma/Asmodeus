def validate_user_input(model_name, is_prompt, prompt):
    if model_name == 'AsmoAI' and prompt != '':
        return ['error', 'Модель не поддерживает текст.']
    elif model_name == None:
        return ['error', 'Модель не выбрана.']
    return ['pass', '']

