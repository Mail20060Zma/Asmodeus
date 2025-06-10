import json
import csv
from datetime import datetime
import os
import copy
import random
import numpy as np
from typing import List, Dict, Set, Tuple
from schedule_validator import ScheduleValidator

def parse_time(time_str):
    """Преобразует строку времени в объект datetime.time"""
    return datetime.strptime(time_str, "%H:%M").time()

def is_online(location):
    """Проверяет, является ли пара онлайн (по URL в месте проведения)"""
    return isinstance(location, str) and location.startswith("http")

def is_teacher_match(teacher_str, desired_teacher):
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

def generate_initial_population(generator, population_size):
    """Генерирует начальную популяцию расписаний"""
    population = []
    for _ in range(population_size):
        if generator.generate_schedule(optimize=False):
            schedule_copy = [list(row) for row in generator.generated_schedule]
            population.append(schedule_copy)
    return population

class GeneticAlgorithm:
    def __init__(self, population_size: int = 50, generations: int = 100):
        self.population_size = population_size
        self.generations = generations
        self.best_schedule = None
        self.best_fitness = float('-inf')
        self.available_auditories = set()  # Множество доступных аудиторий

    def set_available_auditories(self, schedule: List):
        """Собирает список реальных аудиторий из расписания"""
        for row in schedule:
            day, time = row[0], row[1]
            slot = (day, time)
            if slot not in self.used_slots:
                self.used_slots.add(slot)
                if len(row) > 2 and row[2].startswith("Ауд."):
                    self.available_auditories.add(row[2])
        if not self.available_auditories:
            # Если не нашли реальных аудиторий, используем базовый набор
            self.available_auditories = {f"Ауд. {i}" for i in range(1, 51)}

    def calculate_fitness(self, schedule: List) -> float:
        """Расчет приспособленности расписания"""
        if not schedule:
            return float('-inf')

        fitness = 0
        # Базовые очки за каждую пару
        fitness += len(schedule) * 10

        # Штраф за пересечения
        time_slots = set()
        for lesson in schedule:
            day, time = lesson[0], lesson[1]
            slot = (day, time)
            if slot in time_slots:
                fitness -= 50  # Большой штраф за пересечения
            time_slots.add(slot)

        # Бонус за равномерное распределение по дням
        days = {}
        for lesson in schedule:
            day = lesson[0]
            days[day] = days.get(day, 0) + 1
        
        # Штраф за неравномерное распределение
        if days:
            avg_lessons = sum(days.values()) / len(days)
            for count in days.values():
                fitness -= abs(count - avg_lessons) * 5

        return fitness

    def select_parents(self, population: List[List], fitness_scores: List[float]) -> Tuple[List, List]:
        """Выбор родителей для скрещивания"""
        # Турнирный отбор
        def tournament_select():
            candidates = random.sample(range(len(population)), 3)
            return max(candidates, key=lambda i: fitness_scores[i])

        parent1_idx = tournament_select()
        parent2_idx = tournament_select()
        while parent2_idx == parent1_idx:
            parent2_idx = tournament_select()

        # Создаем копии родителей без использования deepcopy
        parent1 = [list(row) for row in population[parent1_idx]]
        parent2 = [list(row) for row in population[parent2_idx]]
        return parent1, parent2

    def crossover(self, parent1: List, parent2: List) -> Tuple[List, List]:
        """Скрещивание двух расписаний"""
        if not parent1 or not parent2:
            return parent1, parent2

        # Точка разрыва
        crossover_point = random.randint(0, min(len(parent1), len(parent2)) - 1)
        
        # Создаем потомков
        child1 = parent1[:crossover_point] + [list(row) for row in parent2[crossover_point:]]
        child2 = parent2[:crossover_point] + [list(row) for row in parent1[crossover_point:]]

        return child1, child2

    def optimize(self, population: list) -> list:
        """Оптимизация расписания с помощью генетического алгоритма"""
        if not population:
            return None
        for generation in range(self.generations):
            fitness_scores = [self.calculate_fitness(schedule) for schedule in population]
            max_fitness_idx = np.argmax(fitness_scores)
            if fitness_scores[max_fitness_idx] > self.best_fitness:
                self.best_fitness = fitness_scores[max_fitness_idx]
                self.best_schedule = [list(row) for row in population[max_fitness_idx]]
            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population, fitness_scores)
                child1, child2 = self.crossover(parent1, parent2)
                new_population.extend([child1, child2])
            population = new_population[:self.population_size]
        return self.best_schedule

class ScheduleGenerator:
    def __init__(self, schedule_file, preferences_file):
        self.schedule_file = schedule_file
        self.preferences_file = preferences_file
        self.original_schedule = None
        self.temp_schedule = None
        self.preferences = None
        self.generated_schedule = []
        self.used_slots = set()
        self.original_subject_count = 0
        self.max_attempts = 100
        self.available_auditories = set()
        self.validator = ScheduleValidator()

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
            csv_data += f"{day},{time},{auditory},{subject},{group},{teacher},{institute}\n"

        # Валидируем расписание
        is_valid = self.validator.validate_schedule(csv_data)
        return is_valid, "Расписание валидно" if is_valid else "Расписание невалидно"

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
                    lesson[0] in self.preferences["undesired_days"] and not is_online(lesson[2])
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
                                if is_teacher_match(lesson[3], desired):
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
                        any(is_teacher_match(lesson[3], teacher) for teacher in self.preferences["desired_teachers"])
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

    def try_add_subject(self, subject, groups):
        """Попытка добавить предмет в расписание"""
        if not groups:
            return False

        # Проверяем, не добавлен ли уже этот предмет
        if any(row[3] == subject for row in self.generated_schedule):
            return False

        # Сначала пробуем группы с онлайн-парами
        online_groups = {
            group: lessons for group, lessons in groups.items()
            if lessons and any(is_online(lesson[2]) for lesson in lessons)
        }
        if online_groups:
            groups = online_groups

        # Пробуем добавить каждую группу
        for attempt in range(self.max_attempts):
            group_keys = [g for g in groups.keys() if groups[g]]
            if not group_keys:
                return False

            # Добавляем рандом: перемешиваем список групп перед выбором
            random.shuffle(group_keys)
            selected_group = random.choice(group_keys)
            success = True
            temp_used_slots = set()

            # Проверяем все пары группы
            for lesson in groups[selected_group]:
                try:
                    if not lesson or len(lesson) < 5:
                        continue
                    day, time, auditory, teacher, institute = lesson
                    key = (day, time)

                    # Онлайн-пары всегда включаются
                    if is_online(auditory):
                        continue
                    # Для обычных пар проверяем пересечения
                    elif key in self.used_slots:
                        success = False
                        break
                    else:
                        temp_used_slots.add(key)
                except Exception as e:
                    success = False
                    break

            # Если все пары подходят, добавляем их в расписание
            if success:
                for lesson in groups[selected_group]:
                    try:
                        if not lesson or len(lesson) < 5:
                            continue
                        day, time, auditory, teacher, institute = lesson
                        key = (day, time)
                        self.generated_schedule.append([day, time, auditory, subject, selected_group, teacher, institute])
                        if not is_online(auditory):
                            self.used_slots.add(key)
                    except Exception as e:
                        pass
                return True

        return False

    def generate_schedule(self, optimize=True):
        try:
            self.generated_schedule = []
            self.used_slots = set()
            self.temp_schedule = {}
            for subject, groups in self.original_schedule.items():
                self.temp_schedule[subject] = {}
                for group, lessons in groups.items():
                    self.temp_schedule[subject][group] = [list(lesson) for lesson in lessons]

            initial_subjects = set(self.temp_schedule.keys())
            self.filter_by_unwanted_days()
            self.filter_by_preferences()
            self.filter_by_institutes()  # Добавляем фильтрацию по институтам
            
            remaining_subjects = set(self.temp_schedule.keys())
            if len(remaining_subjects) < len(initial_subjects):
                return False

            sorted_subjects = self.sort_subjects_by_lessons()
            for subject in sorted_subjects:
                if subject not in self.temp_schedule:
                    continue
                
                groups = self.temp_schedule[subject]
                if not groups:
                    continue
            
                if not self.try_add_subject(subject, groups):
                    original_groups = self.original_schedule[subject]
                    if not self.try_add_subject(subject, original_groups):
                        continue
            
            scheduled_subjects = set(row[3] for row in self.generated_schedule if row[3])
            if len(scheduled_subjects) != self.original_subject_count:
                return False

            return True
        except Exception as e:
            return False

    def save_schedule(self, output_file):
        """Сохраняет расписание в CSV файл"""
        try:
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)  # Заключаем все поля в кавычки
                # Записываем заголовки
                writer.writerow(['Day', 'Time', 'Auditory', 'Subject', 'Group', 'Teacher', 'Institute'])
                # Записываем данные
                for lesson in self.generated_schedule:
                    writer.writerow(lesson)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении расписания: {e}")
            return False

def generate_schedule(schedule_data, preferences, num_variants=5):
    """
    Генерирует варианты расписания с учетом предпочтений
    """
    variants = []
    for _ in range(num_variants):
        # Создаем копию данных для текущего варианта
        current_schedule = schedule_data.copy()
        
        # Словарь для отслеживания выбранных групп для каждого предмета
        subject_groups = {}
        
        # Словарь для отслеживания занятых временных слотов для каждой группы
        group_time_slots = {}
        
        # Словарь для отслеживания дней с занятиями для каждой группы
        group_days = {}
        
        # Перемешиваем строки для случайного выбора
        rows = list(current_schedule.items())
        random.shuffle(rows)
        
        # Обрабатываем каждую строку
        for key, row in rows:
            subject = row['Subject']
            group = row['Group']
            day = row['Day']
            time = row['Time']
            auditory = row['Auditory']  # Сохраняем оригинальное значение аудитории
            
            # Проверяем, выбрана ли уже группа для этого предмета
            if subject in subject_groups and subject_groups[subject] != group:
                continue
            
            # Проверяем, занят ли временной слот для этой группы
            if group in group_time_slots and (day, time) in group_time_slots[group]:
                continue
            
            # Если группа еще не выбрана для этого предмета, выбираем ее
            if subject not in subject_groups:
                subject_groups[subject] = group
            
            # Если группа еще не имеет занятых временных слотов, инициализируем
            if group not in group_time_slots:
                group_time_slots[group] = set()
            
            # Добавляем временной слот для группы
            group_time_slots[group].add((day, time))
            
            # Если группа еще не имеет дней с занятиями, инициализируем
            if group not in group_days:
                group_days[group] = set()
            
            # Добавляем день для группы
            group_days[group].add(day)
            
            # Сохраняем оригинальное значение аудитории
            row['Auditory'] = auditory
        
        # Сортируем строки по дню и времени
        sorted_schedule = dict(sorted(current_schedule.items(), key=lambda x: (x[1]['Day'], x[1]['Time'])))
        
        variants.append(sorted_schedule)
    
    return variants

def main():
    # Получаем путь к корневой директории проекта
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Пути к файлам
    schedule_file = os.path.join(root_path, 'data', 'schedules', 'database', 'schedule.json')
    preferences_file = os.path.join(root_path, 'data', 'schedules', 'database', 'Preferences.json')
    output_dir = os.path.join(root_path, 'data', 'schedules', 'ready')
    
    # Создаем директорию для выходных файлов, если она не существует
    os.makedirs(output_dir, exist_ok=True)
    
    generator = ScheduleGenerator(schedule_file, preferences_file)
    if not generator.load_data():
        print("\nОШИБКА: Не удалось загрузить данные из файлов")
        return

    # Параметры для генерации
    num_schedules = 5
    population_size = 20
    generations = 50
    
    successful_schedules = 0
    unique_schedules = set()
    max_attempts = 50

    attempt = 0
    while successful_schedules < num_schedules and attempt < max_attempts:
        attempt += 1
        
        # Генерируем начальную популяцию
        population = []
        for _ in range(population_size):
            if generator.generate_schedule(optimize=False):
                schedule_copy = [list(row) for row in generator.generated_schedule]
                # Проверяем валидность расписания
                is_valid, _ = generator.validate_schedule(schedule_copy)
                if is_valid:
                    population.append(schedule_copy)
        
        if not population:
            continue

        # Оптимизируем расписание
        genetic = GeneticAlgorithm(population_size, generations)
        genetic.available_auditories = generator.available_auditories
        best_schedule = genetic.optimize(population)
        
        if best_schedule:
            # Проверяем валидность лучшего расписания
            is_valid, _ = generator.validate_schedule(best_schedule)
            if not is_valid:
                continue

            schedule_str = str(sorted(best_schedule))
            
            if schedule_str not in unique_schedules:
                unique_schedules.add(schedule_str)
                generator.generated_schedule = best_schedule
                output_file = os.path.join(output_dir, f"schedule_variant_{successful_schedules + 1}.csv")
                
                if generator.save_schedule(output_file):
                    successful_schedules += 1

    if successful_schedules == 0:
        print("\nОШИБКА: Не удалось сгенерировать ни одного расписания")
    else:
        print(f"\nУспешно сгенерировано расписаний: {successful_schedules} из {num_schedules}")

if __name__ == "__main__":
    main()