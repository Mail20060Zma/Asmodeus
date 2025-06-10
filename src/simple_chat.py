import requests
import json
import os

# Константы
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"

def load_schedule_data():
    """
    Загружает данные расписания из JSON файла
    """
    try:
        with open('schedule.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка при загрузке расписания: {str(e)}")
        return None

def send_message(message):
    """
    Отправляет одно сообщение в API и получает ответ
    
    Args:
        message (str): Сообщение пользователя
    """
    try:
        response = requests.post(
            url=API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-chat-v3-0324:free",
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            })
        )
        
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
        
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return None

def main():
    # Загрузка данных расписания
    schedule_data = load_schedule_data()
    if not schedule_data:
        print("Не удалось загрузить данные расписания")
        return

    # Базовый промпт
    base_prompt = """
{
  "task": "generate_schedule",
  "input_format": "nested_subjects_json",
  "output_format": "CSV",
  "constraints": {
    "one_group_per_subject": true,
    "include_all_selected_pairs": true,
    "no_time_conflicts": true,
    "online_classes_always_include_at": ["06:30", "20:50"],
    "teachers_separator": ", "
  },
  "preferences": {
    "desired_days": [],
    "undesired_days": ["Monday"],
    "desired_groups": {
      "Дополнительные главы математики. ИРИТ-РТФ (09 УГН)": ["АТ-16"]
    },
    "undesired_groups": {
    },
    "desired_teachers": [],
    "undesired_teachers": [],
    "time_priority": "",
    "min_start_time": "08:30",
    "min_end_time": "18:00"
  },
  "selection_priority_order": [
    "online_time_override",
    "desired_teachers",
    "undesired_teachers",
    "desired_groups",
    "undesired_groups",
    "desired_days",
    "undesired_days",
    "time_priority",
    "min_start_time",
    "min_end_time"
  ],
  "output_csv_format": {
    "encoding": "UTF-8",
    "delimiter": ",",
    "quote_all_fields": true,
    "columns": [
        "Day",
        "Time",
        "Auditory",
        "Subject",
        "Group",
        "Teacher"
    ]
  },
  "error_handling": {
    "if_no_schedule": "Расписание не найдено: конфликты предпочтений"
  },
  "examples": {
    "subjects": {
      "Физика": {
        "АТ-40": [["Пн", "08:30", "И101", "Иванов"]],
        "АТ-36": [["Чт", "12:00", "И201", "Сидоров"]]
      },
      "Математика": {
        "АТ-41": [["Ср", "10:15", "А201", "Петров"]],
        "АТ-42": [["Ср", "12:00", "А202", "Иванов"]]
      }
    }
  }
}

"""

    # Добавляем данные расписания в промпт
    schedule_prompt = f"{base_prompt}\n\nДанные расписания:\n{json.dumps(schedule_data, ensure_ascii=False, indent=2)}"
    
    # Отправляем запрос к API
    response = send_message(schedule_prompt)
    if response:
        print("\nОтвет ИИ:")
        print(response)

if __name__ == "__main__":
    main() 