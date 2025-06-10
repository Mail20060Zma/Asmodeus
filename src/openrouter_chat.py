import requests
import json
import textwrap
import os
from datetime import datetime

# Константы
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"
HISTORY_FILE = "chat_history.json"

def load_history():
    """
    Загружает историю переписки из файла
    """
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка при загрузке истории: {e}")
    return []

def save_history(messages):
    """
    Сохраняет историю переписки в файл
    """
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении истории: {e}")

def format_response(response_data):
    """
    Форматирует ответ API в читаемый вид
    
    Args:
        response_data (dict): Данные ответа от API
    """
    try:
        # Получаем основную информацию
        model = response_data.get('model', 'Неизвестная модель')
        created = response_data.get('created', 'Неизвестное время')
        
        # Получаем сообщение ассистента
        message = response_data.get('choices', [{}])[0].get('message', {}).get('content', 'Нет ответа')
        
        # Получаем статистику использования токенов
        usage = response_data.get('usage', {})
        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)
        total_tokens = usage.get('total_tokens', 0)
        
        # Форматируем вывод
        print("\n" + "="*80)
        print(f"Модель: {model}")
        print(f"Время создания: {created}")
        print("-"*80)
        print("Ответ ассистента:")
        print("-"*80)
        
        # Обрабатываем сообщение, выделяя блоки кода
        lines = message.split('\n')
        in_code_block = False
        for line in lines:
            if line.startswith('```'):
                in_code_block = not in_code_block
                print("-"*80 if not in_code_block else "")
                continue
            if in_code_block:
                print(f"    {line}")
            else:
                # Оборачиваем текст для лучшей читаемости
                wrapped_text = textwrap.fill(line, width=76)
                print(wrapped_text)
        
        print("-"*80)
        print("Статистика токенов:")
        print(f"├─ Токены в запросе: {prompt_tokens}")
        print(f"├─ Токены в ответе: {completion_tokens}")
        print(f"└─ Всего токенов: {total_tokens}")
        print("="*80 + "\n")
        
        return message
        
    except Exception as e:
        print("\n" + "!"*80)
        print("ОШИБКА ПРИ ОБРАБОТКЕ ОТВЕТА")
        print("!"*80)
        print(f"Тип ошибки: {type(e).__name__}")
        print(f"Описание ошибки: {str(e)}")
        print("-"*80)
        print("Исходный ответ API:")
        print("-"*80)
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
        print("!"*80 + "\n")
        return None

def send_message(messages):
    """
    Отправляет сообщение в API и получает ответ
    
    Args:
        messages (list): Список сообщений в формате [{"role": "user", "content": "..."}, ...]
    """
    try:
        response = requests.post(
            url=API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "qwen/qwen3-235b-a22b:free",
                "messages": messages
            })
        )
        
        # Проверяем статус ответа
        response.raise_for_status()
        
        # Форматируем и выводим ответ
        return format_response(response.json())
        
    except requests.exceptions.RequestException as e:
        print("\n" + "!"*80)
        print("ОШИБКА ПРИ ВЫПОЛНЕНИИ API ЗАПРОСА")
        print("!"*80)
        print(f"Код ответа: {e.response.status_code if hasattr(e, 'response') else 'N/A'}")
        print(f"Тип ошибки: {type(e).__name__}")
        print(f"Описание ошибки: {str(e)}")
        if hasattr(e, 'response'):
            print("-"*80)
            print("Ответ сервера:")
            print("-"*80)
            try:
                print(json.dumps(e.response.json(), indent=2, ensure_ascii=False))
            except:
                print(e.response.text)
        print("!"*80 + "\n")
        return None

def main():
    # Загружаем историю переписки
    messages = load_history()
    
    # Если история пуста, добавляем системное сообщение
    if not messages:
        messages.append({
            "role": "system",
            "content": "Ты - полезный ассистент, который помогает пользователю с его вопросами."
        })
    
    print("Чат запущен. Введите 'выход' для завершения или 'очистить' для очистки истории.")
    
    while True:
        user_input = input("\nВы: ").strip()
        
        if user_input.lower() in ['выход', 'exit', 'quit']:
            break
        elif user_input.lower() in ['очистить', 'clear']:
            messages = [messages[0]]  # Оставляем только системное сообщение
            save_history(messages)
            print("История переписки очищена.")
            continue
        
        # Добавляем сообщение пользователя в историю
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Отправляем запрос с историей переписки
        response = send_message(messages)
        
        if response:
            # Добавляем ответ ассистента в историю
            messages.append({
                "role": "assistant",
                "content": response
            })
            # Сохраняем обновленную историю
            save_history(messages)
    
    print("\nСеанс завершён. История переписки сохранена.")

if __name__ == "__main__":
    main()