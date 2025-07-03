def validate_user_input(model_name, is_prompt, prompt, settings):
    if model_name == 'AsmoAI(no text)' and prompt != '':
        return ['error', 'Модель не поддерживает текст.']
    elif model_name == None:
        return ['error', 'Модель не выбрана.']
    elif model_name == 'AsmoAI(no text)' and settings['AsmoAI_warning'] != True:
        return ['warning', 'Вы собираетесь использовать AsmoAI./Это НЕ ИИ, это АЛГОРИТМ./Он сгенерирует 5 вариантов расписания.']
    elif prompt != '' and settings['TextPrompt_warning'] != True:
        return ['warning', 'Вы собираетесь использовать текстовый промпт./К сожалению, эта функция очень нестабильна/и часто приводит к сбоям в генерации./Рекомендуем использовать ручные переключатели.']
    elif not is_prompt and settings['NoPrompt_warning'] != True:
        return ['warning','Вы не использовали дополнительных настроек./Это увеличивает шансы на сбой генерации./Рекомендуем выбрать хотя бы пару параметров.']
    return ['pass', '']

