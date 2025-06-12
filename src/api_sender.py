import json
import random
import os
from typing import Dict, Any, Optional
import requests
from pathlib import Path
import aiohttp
import asyncio
from datetime import datetime
from schedule_validator import ScheduleValidator

class APISender:
    def __init__(self):
        self.config_dir = Path(__file__).parent / 'config'
        self.models_config = self._load_json('api_model.json')
        self.api_keys = self._load_json('api_keys.json')
        self.schedule_data = self._load_schedule_data()
        self.schedule_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'schedules', 'database', 'schedule.json')
        self.preferences_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'schedules', 'database', 'preferences.json')
        self.validator = ScheduleValidator()
        self.original_schedule: Dict = {}
        self.preferences: Dict = {}
        self.validator = ScheduleValidator()
        
    def _load_json(self, filename: str) -> Dict[str, Any]:
        """Загрузка JSON файла из конфигурационной директории"""
        file_path = self.config_dir / filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл конфигурации {filename} не найден в {self.config_dir}")
        except json.JSONDecodeError:
            raise ValueError(f"Ошибка в формате JSON файла {filename}")

    def _get_random_api_key(self) -> str:
        """Получение случайного API ключа из списка"""
        if not self.api_keys:
            raise ValueError("Список API ключей пуст")
        return random.choice(self.api_keys)

    def _get_model_id(self, model_name: Optional[str] = None) -> str:
        """Получение ID модели"""
        if model_name is None:
            model_name = self.models_config.get('default_model')
        
        model_id = self.models_config['models'].get(model_name)
        if not model_id:
            raise ValueError(f"Модель {model_name} не найдена в конфигурации")
        
        return model_id

    def _load_schedule_data(self):
        schedule_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'schedules', 'database', 'schedule.json')
        with open(schedule_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def is_teacher_match(self, teacher_str, desired_teacher):
        """Проверяет совпадение преподавателя (полное ФИО, фамилия с инициалами или только фамилия)"""
        if not teacher_str or not desired_teacher:
            return False
        teacher_parts = [t.strip() for t in teacher_str.split(",")]
        desired_parts = desired_teacher.split()
        for teacher in teacher_parts:
            teacher_words = teacher.split()
            # Проверяем полное совпадение
            if desired_teacher in teacher:
                return True
            # Проверяем совпадение фамилии
            if desired_parts[0] == teacher_words[0]:
                return True
            # Проверяем совпадение инициалов только если количество слов совпадает
            if len(teacher_words) == len(desired_parts):
                if all(part[0] == desired_parts[i][0] for i, part in enumerate(teacher_words)):
                    return True
        return False

    def load_data(self) -> tuple:
        """Загрузка исходных данных из файлов"""
        try:
            with open(self.schedule_file, 'r', encoding='utf-8') as f:
                self.original_schedule = json.load(f)
            
            with open(self.preferences_file, 'r', encoding='utf-8') as f:
                self.preferences = json.load(f)
            
            return (original_schedule, preferences)
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            return (None, None)

    def filter_by_undesired_time(self) -> None:
        """Фильтрация по нежелательному времени"""
        if not self.preferences.get("undesired_time"):
            return

        for subject in list(self.filtered_schedule.keys()):
            for group in list(self.filtered_schedule[subject].keys()):
                lessons = self.filtered_schedule[subject][group]
                has_unwanted_time = False
                for lesson in lessons:
                    day = lesson[0]
                    time = lesson[1].lstrip("0").replace(":", "_")
                    if day in self.preferences["undesired_time"]:
                        if time in self.preferences["undesired_time"][day]:
                            has_unwanted_time = True
                            break
                
                if has_unwanted_time:
                    del self.filtered_schedule[subject][group]

    def _is_teacher_match(self, teacher_str: str, desired_teacher: str) -> bool:
        """Проверка совпадения преподавателя"""
        if not teacher_str or not desired_teacher:
            return False
            
        teacher_parts = [t.strip() for t in teacher_str.split(",")]
        desired_parts = desired_teacher.split()
        
        for teacher in teacher_parts:
            teacher_words = teacher.split()
            # Проверяем полное совпадение
            if desired_teacher in teacher:
                return True
            # Проверяем совпадение фамилии
            if desired_parts[0] == teacher_words[0]:
                return True
            # Проверяем совпадение инициалов
            if len(teacher_words) == len(desired_parts):
                if all(part[0] == desired_parts[i][0] for i, part in enumerate(teacher_words)):
                    return True
        return False

    def filter_by_desired_groups(self) -> None:
        """Фильтрация по желаемым группам и преподавателям"""
        if not self.preferences.get("desired_groups"):
            return

        for subject in list(self.filtered_schedule.keys()):
            if subject in self.preferences["desired_groups"]:
                desired_list = self.preferences["desired_groups"][subject]
                filtered_groups = {}
                
                for group, lessons in self.filtered_schedule[subject].items():
                    # Проверяем, является ли группа одной из желаемых
                    if group in desired_list:
                        filtered_groups[group] = lessons
                        continue
                    
                    # Проверяем, есть ли желаемый преподаватель в занятиях группы
                    for lesson in lessons:
                        for desired in desired_list:
                            if self._is_teacher_match(lesson[3], desired):
                                filtered_groups[group] = lessons
                                break
                
                self.filtered_schedule[subject] = filtered_groups

    def filter_by_undesired_institutes(self) -> None:
        """Фильтрация по нежелательным институтам"""
        if not self.preferences.get("undesired_institutes"):
            return

        for subject in list(self.filtered_schedule.keys()):
            for group in list(self.filtered_schedule[subject].keys()):
                lessons = self.filtered_schedule[subject][group]
                has_unwanted_institute = any(
                    lesson[4] in self.preferences["undesired_institutes"]
                    for lesson in lessons
                )
                if has_unwanted_institute:
                    del self.filtered_schedule[subject][group]

    def sort_subjects_by_groups_count(self) -> None:
        """Сортировка предметов по количеству групп"""
        self.filtered_schedule = dict(sorted(
            self.filtered_schedule.items(),
            key=lambda x: len(x[1])
        ))

    def check_subjects_have_groups(self) -> bool:
        """Проверка наличия хотя бы одной группы для каждого предмета"""
        return all(len(groups) > 0 for groups in self.filtered_schedule.values())

    def save_validated_schedule(self, schedule_data: str, output_file: str) -> bool:
        """
        Сохраняет расписание только если оно прошло валидацию
        
        Args:
            schedule_data (str): Расписание в формате CSV
            output_file (str): Путь к файлу для сохранения
            
        Returns:
            bool: True если расписание сохранено, False если не прошло валидацию
        """
        try:
            # Проверяем валидность расписания
            is_valid = self.validator.validate_schedule(schedule_data)
            
            if not is_valid:
                print("Расписание не прошло валидацию")
                return False
                
            # Если расписание валидно, сохраняем его
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                f.write(schedule_data)
            print(f"Расписание успешно сохранено в {output_file}")
            return True
            
        except Exception as e:
            print(f"Ошибка при сохранении расписания: {e}")
            return False

    def send_message(self, model_name = "Llama"):
        self.load_data()
        self.filtered_schedule = self.original_schedule.copy()
        # Применяем фильтры
        self.filter_by_undesired_time()
        self.filter_by_desired_groups()
        self.filter_by_undesired_institutes()

        if not self.check_subjects_have_groups():
            print("Ошибка: не все предметы имеют доступные группы после фильтрации")
            return False
        
        api_key = self._get_random_api_key()
        model_id = self._get_model_id(model_name)
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/yourusername/your-repo",
            "X-Title": "Asmodeus Project"
        }
        data = {
            "model": model_id,
            "messages": [
                {
                    "role": "system",
                    "content": """
▌ Система генерации учебных расписаний Asmodeus
▌ Версия: 2.1 | Формат: Strict-CSV

▼ Цель системы:
Автоматически генерировать оптимальные расписания без временных конфликтов, учитывая:
1. Выбор ровно ОДНОЙ группы для каждого предмета
2. Для каждой группы выберать все пары 
3. Запрет временных пересечений (день+время)

▼ Входные данные (JSON):
{\n  "Предмет": {\n    "Группа": [\n      [Day,Time,Auditory,Teacher,Institute]\n    ]\n  }\n}\n
▼ Требования к обработке:
1. Выбор ровно ОДНОЙ группы для каждого предмета
2. Для каждой группы выберать все пары 
3. Запрет временных пересечений (день+время)


▼ Примеры НЕВЕРНЫХ записей:
["Monday", "10:15", "А-101", "", "Институт 1"]  ← Отсутствует преподаватель

▼ Формат вывода (CSV):
"Day","Time","Auditory","Subject","Group","Teacher","Institute"
""Monday","08:30","А-101","Математика","Группа 1","Иванов А.А.","Институт 1"

▼ Валидация:
Автоматическая проверка:
✓ Наличие всех обязательных полей
✓ Корректность форматов времени
✓ Отсутствие конфликтов

▌! ВСЕ значения в кавычках, кодировка UTF-8
"""
                },
                {
                    "role": "user",
                    "content": json.dumps(self.filtered_schedule, ensure_ascii=False, indent=2)
                }
            ],
            "temperature": 0.1,
            "max_tokens": 3000
        }
        print("Отправляем запрос к API...")

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    schedule_data = result['choices'][0]['message']['content']
                    
                    output_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                             'data', 'schedules', 'ready', 'schedule_variant_1.csv')
                    
                    if self.save_validated_schedule(schedule_data, output_file):
                        print("Расписание успешно сгенерировано и сохранено")
                    else:
                        print("Расписание не прошло валидацию и не было сохранено")
                    
                    return schedule_data
                else:
                    raise Exception("Неверный формат ответа от API")
            else:
                error_text = response.text
                raise Exception(f"Ошибка при отправке сообщения: {error_text}")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            return None

    def validate_schedule(self, schedule):
        """Проверяет валидность расписания используя ScheduleValidator"""
        if not schedule:
            return False, "Расписание пустое"

        # Конвертируем расписание в CSV формат
        csv_data = "Day,Time,Auditory,Subject,Group,Teacher,Institute\n"
        for lesson in schedule:
            # Обрабатываем каждый параметр, заключая его в кавычки
            day = f'"{lesson[0]}"'
            time = f'"{lesson[1]}"'
            auditory = f'"{lesson[2]}"'
            subject = f'"{lesson[3]}"'
            group = f'"{lesson[4]}"'
            teacher = f'"{lesson[5]}"'
            institute = f'"{lesson[6]}"'
            
            # Формируем строку CSV с кавычками
            csv_data += f"'{day}','{time}','{auditory}','{subject}','{group}','{teacher}','{institute}'\n"

        # Валидируем расписание
        is_valid = self.validator.validate_schedule(csv_data)
        return is_valid, "Расписание валидно" if is_valid else "Расписание невалидно"

