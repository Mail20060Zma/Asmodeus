import json
import csv
import os
import io
from typing import Dict, List, Set

def compare_teachers(teacher1, teacher2):
    set1 = set(map(str.strip, teacher1.split(',')))
    set2 = set(map(str.strip, teacher2.split(',')))
    return set1 == set2

class ScheduleValidator:
    def __init__(self):
        self.original_schedule_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'schedules', 'database', 'schedule.json')

    def convert_csv_to_json(self, csv_data):
        """Конвертирует CSV данные в JSON формат с иерархией: предмет -> группа -> [день, время, аудитория, преподаватель, институт]"""
        try:
            if isinstance(csv_data, str):
                csv_file = io.StringIO(csv_data)
            else:
                csv_file = csv_data

            reader = csv.reader(csv_file)
            headers = next(reader)
            data = {}
            for row in reader:
                row_dict = dict(zip(headers, row))
                subject = row_dict.get('Subject', '').replace('\\','')
                group = row_dict.get('Group', '')
                if subject and group:
                    if subject not in data:
                        data[subject] = {}
                    if group not in data[subject]:
                        data[subject][group] = []
                    day = row_dict.get('Day', '')
                    time = row_dict.get('Time', '')
                    auditory = row_dict.get('Auditory', '')
                    teacher = row_dict.get('Teacher', '')
                    institute = row_dict.get('Institute', '')
                    data[subject][group].append([day, time, auditory, teacher, institute])
            return data
        except Exception as e:
            print(f"Ошибка при конвертации: {e}")
            return {}

    def validate_schedule(self, schedule_input):
        """
        Проверяет расписание на соответствие требованиям.
        schedule_input может быть путем к файлу или строкой CSV.
        """
        try:
            with open(self.original_schedule_file, 'r', encoding='utf-8') as f:
                original_schedule = json.load(f)
                original_schedule = {subject.replace('\\',''): groups for subject, groups in original_schedule.items()}
            
            if isinstance(schedule_input, str):
                if os.path.exists(schedule_input):
                    with open(schedule_input, 'r', encoding='utf-8') as f:
                        schedule = self.convert_csv_to_json(f)
                else:
                    schedule = self.convert_csv_to_json(schedule_input)
            else:
                schedule = self.convert_csv_to_json(schedule_input)
            
            if not schedule:
                print("Ошибка: не удалось загрузить расписание")
                return False
            
            if len(schedule) != len(original_schedule):
                print(f"Ошибка: количество предметов не совпадает. Ожидалось {len(original_schedule)}, получено {len(schedule)}")
                return False
            
            for subject, groups in schedule.items():
                if len(groups) != 1:
                    print(f"Ошибка: у предмета {subject} должно быть ровно одна группа, получено {len(groups)}")
                    return False
            
            time_slots = set() 
            for subject, groups in schedule.items():
                if subject not in original_schedule:
                    print(f"Ошибка: предмет {subject} не найден в исходном расписании")
                    return False
                for group, lessons in groups.items():
                    if group not in original_schedule[subject]:
                        print(f"Ошибка: группа {group} не найдена в исходном расписании для предмета {subject}")
                        return False
                    
                    orig_lessons = original_schedule[subject][group]
                    if len(lessons) != len(orig_lessons):
                        print(f"Ошибка: количество пар для {subject} - {group} не совпадает с исходным расписанием")
                        return False

                    orig_lessons_dict = {(l[0], l[1]): l for l in orig_lessons}
                    
                    for lesson in lessons:
                        day, time = lesson[0], lesson[1]
                        slot = (day, time)
                        
                        if slot in time_slots:
                            print(f"Ошибка: временное пересечение для предмета {subject}, группы {group} в день {day}, время {time}")
                            return False
                        time_slots.add(slot)
                        
                        if slot not in orig_lessons_dict:
                            print(f"Ошибка: пара {day} {time} не найдена в исходном расписании для {subject} - {group}")
                            return False
                        
                        orig_lesson = orig_lessons_dict[slot]
                        
                        if len(lesson) != 5 or len(orig_lesson) != 5:
                            print(f"Ошибка: неверное количество параметров для пары {subject} - {group} в {day} {time}")
                            return False
                        
                        if lesson[0] != orig_lesson[0] or lesson[1] != orig_lesson[1]:
                            print(f"Ошибка: несовпадение дня/времени для {subject} - {group} в {day} {time}")
                            return False
                        
                        if lesson[2] != orig_lesson[2]:
                            print(f"Ошибка: несовпадение аудитории для {subject} - {group} в {day} {time}")
                            return False
                        
                        if not compare_teachers(lesson[3], orig_lesson[3]):
                            print(f"Ошибка: несовпадение преподавателя для {subject} - {group} в {day} {time}")
                            return False
                        
                        if lesson[4] != orig_lesson[4]:
                            print(f"Ошибка: несовпадение института для {subject} - {group} в {day} {time}")
                            return False
            
            return True
            
        except Exception as e:
            print(f"Ошибка при проверке расписания: {e}")
            return False


"""
validator = ScheduleValidator()

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
schedule_file = os.path.join(project_root, 'data', 'schedules', 'ready', 'schedule_variant_1.csv')    
is_valid = validator.validate_schedule(schedule_file)


validator = ScheduleValidator()
csv_string = '''Day,Time,Auditory,Subject,Group,Teacher,Institute
Tuesday,14:15,СП501,Дополнительные главы математики. ИРИТ-РТФ (09 УГН),АТ-16,Агафонов Александр Петрович,ИСА'''
is_valid = validator.validate_schedule(csv_string)
"""