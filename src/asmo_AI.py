import json
import os
import random
from typing import Dict, List, Set, Tuple, Optional
from datetime import datetime
from schedule_validator import ScheduleValidator

class AsmodeusAI:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.schedule_path = os.path.join(self.base_path, 'data', 'schedules', 'database', 'schedule.json')
        self.preferences_path = os.path.join(self.base_path, 'data', 'schedules', 'database', 'Preferences.json')
        self.output_path = os.path.join(self.base_path, 'data', 'schedules', 'ready')
        
        self.original_schedule: Dict = {}
        self.preferences: Dict = {}
        self.filtered_schedule: Dict = {}
        self.validator = ScheduleValidator()
        
        os.makedirs(self.output_path, exist_ok=True)

    def load_data(self) -> bool:
        """Загрузка исходных данных из файлов"""
        try:
            with open(self.schedule_path, 'r', encoding='utf-8') as f:
                self.original_schedule = json.load(f)
            
            with open(self.preferences_path, 'r', encoding='utf-8') as f:
                self.preferences = json.load(f)
            
            return True
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            return False

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

    def filter_by_desired_groups(self) -> None:
        """Фильтрация по желаемым группам и преподавателям"""
        if not self.preferences.get("desired_groups"):
            return

        for subject in list(self.filtered_schedule.keys()):
            if subject in self.preferences["desired_groups"]:
                desired_list = self.preferences["desired_groups"][subject]
                filtered_groups = {}
                
                for group, lessons in self.filtered_schedule[subject].items():
                    if group in desired_list:
                        filtered_groups[group] = lessons
                        continue
                    
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

    def _is_teacher_match(self, teacher_str: str, desired_teacher: str) -> bool:
        """Проверка совпадения преподавателя"""
        if not teacher_str or not desired_teacher:
            return False
            
        teacher_parts = [t.strip() for t in teacher_str.split(",")]
        desired_parts = desired_teacher.split()
        
        for teacher in teacher_parts:
            teacher_words = teacher.split()
            if desired_teacher in teacher:
                return True
            if desired_parts[0] == teacher_words[0]:
                return True
            if len(teacher_words) == len(desired_parts):
                if all(part[0] == desired_parts[i][0] for i, part in enumerate(teacher_words)):
                    return True
        return False

    def check_subjects_have_groups(self) -> bool:
        """Проверка наличия хотя бы одной группы для каждого предмета"""
        return all(len(groups) > 0 for groups in self.filtered_schedule.values())

    def sort_subjects_by_groups_count(self) -> None:
        """Сортировка предметов по количеству групп"""
        self.filtered_schedule = dict(sorted(
            self.filtered_schedule.items(),
            key=lambda x: len(x[1])
        ))

    def generate_schedule_variant(self) -> Optional[Dict]:
        """Генерация одного варианта расписания"""
        schedule = {}
        used_time_slots = set()

        for subject, groups in self.filtered_schedule.items():
            available_groups = list(groups.keys())
            random.shuffle(available_groups)
            
            for group in available_groups:
                lessons = groups[group]
                has_conflict = False
                
                for lesson in lessons:
                    time_slot = (lesson[0], lesson[1])
                    if time_slot in used_time_slots:
                        has_conflict = True
                        break
                
                if not has_conflict:
                    schedule[subject] = {group: lessons}
                    for lesson in lessons:
                        used_time_slots.add((lesson[0], lesson[1]))
                    break
            
            if subject not in schedule:
                return None

        return schedule

    def save_schedule_variant(self, schedule: Dict, variant_number: int) -> bool:
        """Сохранение варианта расписания в CSV формате"""
        try:
            output_file = os.path.join(self.output_path, f'schedule_variant_{variant_number}.csv')
            
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                f.write('Day,Time,Auditory,Subject,Group,Teacher,Institute\n')
                
                for subject, groups in schedule.items():
                    for group, lessons in groups.items():
                        for lesson in lessons:
                            day, time, auditory, teacher, institute = lesson
                            f.write(f'"{day}","{time}","{auditory}","{subject}","{group}","{teacher}","{institute}"\n')
            
            return True
        except Exception as e:
            print(f"Ошибка при сохранении расписания: {e}")
            return False

    def generate_schedules(self, num_variants: int = 5, max_attempts: int = 50) -> bool:
        """Генерация нескольких вариантов расписания"""
        if not self.load_data():
            return False

        self.filtered_schedule = self.original_schedule.copy()

        self.filter_by_undesired_time()
        self.filter_by_desired_groups()
        self.filter_by_undesired_institutes()

        if not self.check_subjects_have_groups():
            print("Ошибка: не все предметы имеют доступные группы после фильтрации")
            return False

        self.sort_subjects_by_groups_count()

        generated_variants = 0
        attempts = 0

        while generated_variants < num_variants and attempts < max_attempts:
            schedule = self.generate_schedule_variant()
            if schedule:
                csv_data = self._schedule_to_csv(schedule)
                if self.validator.validate_schedule(csv_data):
                    if self.save_schedule_variant(schedule, generated_variants + 1):
                        generated_variants += 1
            attempts += 1

        return generated_variants == num_variants

    def _schedule_to_csv(self, schedule: Dict) -> str:
        """Конвертация расписания в CSV формат"""
        csv_lines = ['Day,Time,Auditory,Subject,Group,Teacher,Institute']
        
        for subject, groups in schedule.items():
            for group, lessons in groups.items():
                for lesson in lessons:
                    day, time, auditory, teacher, institute = lesson
                    csv_lines.append(f'"{day}","{time}","{auditory}","{subject}","{group}","{teacher}","{institute}"')

        return '\n'.join(csv_lines)

ai = AsmodeusAI()
success = ai.generate_schedules()
if success:
    print("Расписания успешно сгенерированы")
else:
    print("Ошибка при генерации расписаний")