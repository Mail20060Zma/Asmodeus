import re
from datetime import datetime
import csv
import os
import json
from bs4 import BeautifulSoup

dataset = {'Monday':{
            '065000':[], #онлайн пара
            '083000':[], # 1-ая пара
            '101500':[], # 2-ая пара
            '120000':[], # 3-ая пара
            '141500':[], # 4-ая пара
            '160000':[], # 5-ая пара
            '174000':[], # 6-ая пара
            '191500':[], # 7-ая пара
            '205000':[] #онлайн пара
           },
           'Tuesday':{
            '065000':[], 
            '083000':[],
            '101500':[],
            '120000':[],
            '141500':[],
            '160000':[],
            '174000':[],
            '191500':[],
            '205000':[]   
           },
           'Wednesday':{
            '065000':[], 
            '083000':[],
            '101500':[],
            '120000':[],
            '141500':[],
            '160000':[],
            '174000':[],
            '191500':[],
            '205000':[]   
           },
           'Thursday':{
            '065000':[], 
            '083000':[],
            '101500':[],
            '120000':[],
            '141500':[],
            '160000':[],
            '174000':[],
            '191500':[],
            '205000':[]   
           },
           'Friday':{
            '065000':[], 
            '083000':[],
            '101500':[],
            '120000':[],
            '141500':[],
            '160000':[],
            '174000':[],
            '191500':[],
            '205000':[]   
           },
           'Saturday':{
            '065000':[], 
            '083000':[],
            '101500':[],
            '120000':[],
            '141500':[],
            '160000':[],
            '174000':[],
            '191500':[],
            '205000':[]   
           },
           }

institutes = {
    'СП':'ИСА',
    'С':'ИСА',
    'Р':'ИРИТ-РТФ',
    'Х':'ИНМИТ-ХТИ',
    'МТ':'ИНМИТ-ХТИ',
    'Э':'ГУК',
    'М':'ГУК',
    'ГУК':'ГУК',
    'И':'ГУК',
    'Б':'ГУК',
    'Т':'УралЭНИН',
    'УГИ':'УГИ',
    'Ф':'ФТИ',
    'https':'ОНЛАЙН',
    '':''
}

class Lesson():
    def __init__(self, subject:str, lesson_type:str, group:int, teacher:list[str], auditory:str, institute:str = None):
        self.subject = subject
        self.lesson_type = lesson_type
        self.group = group
        self.teacher = teacher
        self.auditory = auditory
        self.institute = institute
    def info(self):
        return(f'{self.lesson_type} по {self.subject} в {self.institute}({self.auditory}) - {self.group}, {self.teacher}')
    
def date_to_weekday(date_str: str) -> str:
    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])
    date = datetime(year, month, day)
    week = [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ]
    return week[date.weekday()]

def convert_subject_shedule(file_path: str) -> None:
    try:
        file = open(file=file_path, encoding='utf-8').readlines()
        worked_data = []
        for string in file:
            if ('DTSTART' in string) or ('SUMMARY' in string) or ('LOCATION' in string) or ('DESCRIPTION' in string):
                if 'DTSTART' in string:
                    string = [date_to_weekday(string.split(':')[1].split('T')[0]), string.split(':')[1].split('T')[1].split('\n')[0]]
                if 'SUMMARY' in string:
                    string = [string.split('/')[0].replace('SUMMARY:',''), string.split('/')[2][-6:].split('\n')[0]]
                if 'LOCATION' in string:
                    string = string.replace('\n','').split(':')[1].replace(' ','')
                    try:
                        string = string.split('/')[1]
                    except:
                        string = string.split('/')[0]
                    # Исправление: если аудитория не определена, подставляем ""
                    if string.lower() in ['неопределено', 'не определено', 'не определена', 'неопределена']:
                        string = ""
                if 'DESCRIPTION' in string:
                    string = [string.split(':')[1].split('/')[0][:-1], string.split(':')[2].replace('\\n\\nПосмотреть в Моем расписании','').replace('\\','')[1:].split(',')]
                worked_data.append(string)
        lessons = [worked_data[i:i+4] for i in range(0, len(worked_data), 4)]
        for lesson in lessons:
            inst = institutes[re.sub(r'[\d-]|\([^)]*\)', '', str(lesson[2]))]
            lsn = Lesson(subject= lesson[1][0],lesson_type= lesson[3][0], group= lesson[1][1],teacher= lesson[3][1], auditory= lesson[2], institute= inst)
            dataset[lesson[0][0]][lesson[0][1]].append(lsn)
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")

def format_time(time_str: str) -> str:
    """Преобразует время из формата HHMMSS в формат HH:MM"""
    hours = time_str[:2]
    minutes = time_str[2:4]
    return f"{hours}:{minutes}"

def export_to_csv(filename="schedule.csv"):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Записываем заголовки
        writer.writerow(['Day', 'Time', 'Auditory', 'Subject', 'Group', 'Teacher', 'Institute'])

        # Проходим по всем дням и времени
        for day, times in dataset.items():
            for time, lessons in times.items():
                # Проходим по всем занятиям в это время
                for lesson in lessons:
                    writer.writerow([
                        day,
                        format_time(time),
                        lesson.auditory,
                        lesson.subject.strip(),
                        lesson.group,
                        ', '.join(lesson.teacher),
                        lesson.institute
                    ])

def process_schedule_files(folder_path):
    """Обрабатывает все файлы .ics в указанной папке."""
    for filename in os.listdir(folder_path):
        if filename.endswith(".ics"):
            file_path = os.path.join(folder_path, filename)
            print(f"Обработка файла: {file_path}")
            convert_subject_shedule(file_path)

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
    
    # Пути к директориям
    data_path = os.path.join(root_path, 'data', 'schedules', 'isc')
    output_path = os.path.join(root_path, 'data', 'schedules', 'database')
    
    # Обрабатываем .ics файлы
    process_schedule_files(data_path)
    
    # Экспортируем в CSV
    csv_file = os.path.join(output_path, 'schedule.csv')
    export_to_csv(csv_file)
    print(f"Расписание экспортировано в {csv_file}")

    # Преобразуем расписание в JSON
    json_file = os.path.join(output_path, 'schedule.json')
    convert_csv_to_json(csv_file, json_file)
    print(f"Расписание также преобразовано в JSON (schedule.json)")

if __name__ == "__main__":
    main()