import csv
import json
import os
from datetime import datetime

def convert_csv_to_json(csv_file, json_file):
    """Конвертирует CSV файл в JSON формат с иерархией: предмет -> группа -> [день, время, аудитория, преподаватель, институт]"""
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            data = {}
            for row in reader:
                row_dict = dict(zip(headers, row))
                subject = row_dict.get('Subject', '')
                group = row_dict.get('Group', '')
                if subject and group:
                    if subject not in data:
                        data[subject] = {}
                    if group not in data[subject]:
                        data[subject][group] = []
                    # Извлекаем дополнительные параметры
                    day = row_dict.get('Day', '')
                    time = row_dict.get('Time', '')
                    auditory = row_dict.get('Auditory', '')
                    teacher = row_dict.get('Teacher', '')
                    institute = row_dict.get('Institute', '')
                    data[subject][group].append([day, time, auditory, teacher, institute])
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")
        return False

def main():
    # Получаем путь к корневой директории проекта
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Пути к файлам
    csv_file = os.path.join(root_path, 'data', 'schedules', 'database', 'schedule.csv')
    json_file = os.path.join(root_path, 'data', 'schedules', 'database', 'schedule.json')
    
    if convert_csv_to_json(csv_file, json_file):
        print(f"Расписание успешно конвертировано из {csv_file} в {json_file}")
    else:
        print("Ошибка при конвертации расписания")

if __name__ == "__main__":
    main() 