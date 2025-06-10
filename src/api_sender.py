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
        self.original_schedule = None
        self.original_subject_count = 0
        self.available_auditories = set()
        self.preferences = {}
        self.temp_schedule = {}
        self.schedule_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'schedules', 'database', 'schedule.json')
        self.preferences_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'schedules', 'database', 'preferences.json')
        self.validator = ScheduleValidator()
        self.load_data()
        
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

    def parse_time(self, time_str):
        """Преобразует строку времени в объект datetime.time"""
        return datetime.strptime(time_str, "%H:%M").time()

    def is_online(self, location):
        """Проверяет, является ли пара онлайн (по URL в месте проведения)"""
        return isinstance(location, str) and location.startswith("http")

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

    def load_data(self):
        """Загрузка данных из JSON файлов"""
        try:
            with open(self.schedule_file, 'r', encoding='utf-8') as f:
                self.original_schedule = json.load(f)
                self.original_subject_count = len(self.original_schedule)
                # Собираем список реальных аудиторий
                for subject, groups in self.original_schedule.items():
                    for group, lessons in groups.items():
                        for lesson in lessons:
                            if len(lesson) > 2 and lesson[2].startswith("Ауд."):
                                self.available_auditories.add(lesson[2])
                # Если не нашли реальных аудиторий, используем базовый набор
                if not self.available_auditories:
                    self.available_auditories = {f"Ауд. {i}" for i in range(1, 51)}
            
            with open(self.preferences_file, 'r', encoding='utf-8') as f:
                self.preferences = json.load(f)
            
            return True
        except Exception as e:
            print(f"Ошибка при загрузке данных: {str(e)}")
            return False

    def filter_by_unwanted_days(self):
        """Фильтрация расписания по нежелательным дням (с исключением онлайн-пар)"""
        if not self.preferences.get("undesired_days"):
            return
        removed_groups = 0
        for subject in list(self.temp_schedule.keys()):
            for group in list(self.temp_schedule[subject].keys()):
                lessons = self.temp_schedule[subject][group]
                has_unwanted_day = any(
                    lesson[0] in self.preferences["undesired_days"] and not self.is_online(lesson[2])
                    for lesson in lessons
                )
                if has_unwanted_day:
                    del self.temp_schedule[subject][group]
                    removed_groups += 1

    def filter_by_preferences(self):
        """Фильтрация по предпочтительным группам и преподавателям"""
        # Фильтрация по desired_groups
        if self.preferences.get("desired_groups"):
            for subject in list(self.temp_schedule.keys()):
                if subject in self.preferences["desired_groups"]:
                    desired_list = self.preferences["desired_groups"][subject]
                    filtered = {}
                    for group, lessons in self.temp_schedule[subject].items():
                        # Если группа явно указана в списке
                        if group in desired_list:
                            filtered[group] = lessons
                        # Если хотя бы один преподаватель из списка есть в занятиях группы
                        for lesson in lessons:
                            for desired in desired_list:
                                if self.is_teacher_match(lesson[3], desired):
                                    filtered[group] = lessons
                                    break
                            if group in filtered:
                                break
                    self.temp_schedule[subject] = filtered
        # Фильтрация по desired_teachers
        if self.preferences.get("desired_teachers"):
            removed_groups = 0
            for subject in list(self.temp_schedule.keys()):
                for group in list(self.temp_schedule[subject].keys()):
                    lessons = self.temp_schedule[subject][group]
                    has_desired_teacher = any(
                        any(self.is_teacher_match(lesson[3], teacher) for teacher in self.preferences["desired_teachers"])
                        for lesson in lessons
                    )
                    if not has_desired_teacher:
                        del self.temp_schedule[subject][group]
                        removed_groups += 1

    def filter_by_institutes(self):
        """Фильтрация расписания по желаемым и нежелаемым институтам"""
        if not self.preferences.get("desired_institutes") and not self.preferences.get("undesired_institutes"):
            return
        removed_groups = 0
        for subject in list(self.temp_schedule.keys()):
            for group in list(self.temp_schedule[subject].keys()):
                lessons = self.temp_schedule[subject][group]
                for lesson in lessons:
                    if not lesson or len(lesson) < 5:
                        continue
                    institute = lesson[4]  # Институт находится в 5-м элементе списка
                    if self.preferences.get("desired_institutes") and institute not in self.preferences["desired_institutes"]:
                        del self.temp_schedule[subject][group]
                        removed_groups += 1
                        break
                    if self.preferences.get("undesired_institutes") and institute in self.preferences["undesired_institutes"]:
                        del self.temp_schedule[subject][group]
                        removed_groups += 1
                        break

    def sort_subjects_by_lessons(self):
        """Сортировка предметов по количеству групп"""
        subject_groups = []
        for subject, groups in self.temp_schedule.items():
            group_count = len(groups)
            subject_groups.append((subject, group_count))
        subject_groups.sort(key=lambda x: x[1])
        small_subjects = [s[0] for s in subject_groups if s[1] < 5]
        other_subjects = [s[0] for s in subject_groups if s[1] >= 5]
        random.shuffle(other_subjects)
        return small_subjects + other_subjects

    def process_schedule_data(self):
        """Полная обработка данных расписания перед отправкой"""
        # Загружаем данные
        if not self.load_data():
            raise Exception("Ошибка загрузки данных")
            
        # Инициализируем временное расписание
        self.temp_schedule = self.original_schedule.copy()
        
        # Применяем фильтры
        self.filter_by_unwanted_days()
        self.filter_by_preferences()
        self.filter_by_institutes()
        
        # Сортируем предметы
        sorted_subjects = self.sort_subjects_by_lessons()
        
        # Создаем новый словарь с отсортированными предметами
        processed_schedule = {}
        for subject in sorted_subjects:
            if subject in self.temp_schedule:
                processed_schedule[subject] = self.temp_schedule[subject]
        
        return processed_schedule

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

    async def send_message(self, model_name="Llama"):
        # Обрабатываем данные перед отправкой
        processed_data = self.process_schedule_data()
        
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
 Ты — алгоритм для генерации оптимального учебного расписания. Обрабатываешь входные данные в JSON-формате и возвращаешь расписание в CSV-формате, где для каждого предмета выбрана ровно одна группа без временных пересечений.

 ▌ Входные данные (JSON-формат):
 ```json
 {
   "Subject": {
     "Group": [
       ["Day", "Time", "Auditory", "Teacher", "Institute"],
       // ... другие пары для этой группы
     ],
     // ... другие группы
   },
   // ... другие предметы
 }
 ▌ Требования к обработке:

 Для каждого предмета выбрать ровно одну группу

 Исключить временные пересечения (одинаковые день+время)

 Минимизировать количество дней с занятиями

 Оптимизировать распределение нагрузки

 ▌ Формат вывода (CSV):

 csv
 Day,Time,Auditory,Subject,Group,Teacher,Institute
 "Понедельник","09:00-10:30","А-101","Математика","Группа 1","Иванов А.А."
 "Вторник","11:00-12:30","Б-205","Физика","Группа 3","Петрова С.И."

 ▌ Пример вывода:

 csv
 Вариант 1:
 Day,Time,Auditory,Subject,Group,Teacher,Institute
 "Понедельник","09:00-10:30","А-101","Математика","Группа 1","Иванов А.А."
 "Среда","14:00-15:30","Б-103","Физика","Группа 2","Сидоров В.П."
 "Пятница","10:00-11:30","А-202","Химия","Группа 1","Петрова С.И."

 Вариант 2:
 Day,Time,Auditory,Subject,Group,Teacher,Institute
 "Вторник","09:00-10:30","А-105","Математика","Группа 2","Смирнов И.Н."
 "Четверг","11:00-12:30","Б-201","Физика","Группа 1","Козлова М.В."
 "Пятница","13:00-14:30","А-305","Химия","Группа 3","Иванов А.А."

 Твой ответ должен содержать только CSV-данные без дополнительных пояснений. Все значения в кавычках, кодировка UTF-8.
 """
                },
                {
                    "role": "user",
                    "content": json.dumps(processed_data, ensure_ascii=False, indent=2)
                }
            ],
            "temperature": 0.1,
            "max_tokens": 3000
        }
        print("Отправляем запрос к API...")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        if 'choices' in result and len(result['choices']) > 0:
                            schedule_data = result['choices'][0]['message']['content']
                            
                            # Сохраняем расписание с проверкой валидации
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
                        error_text = await response.text()
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

