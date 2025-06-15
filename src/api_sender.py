import json
import random
import os
from typing import Dict, Any, Optional
import aiohttp
import asyncio
from schedule_validator import ScheduleValidator

class APISender:
    def __init__(self):
        self.config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),  'config')
        self.models_config = self._load_json('api_model.json')
        self.api_keys = self._load_json('api_keys.json')
        self.schedule_data = self._load_schedule_data()
        self.schedule_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'schedules', 'database', 'schedule.json')
        self.preferences_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'schedules', 'database', 'preferences.json')
        self.validator = ScheduleValidator()
        self.original_schedule: Dict = {}
        self.preferences: Dict = {}
        self.validator = ScheduleValidator()
        self.semaphore = asyncio.Semaphore(1000)
        
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

    def load_data(self) -> tuple:
        """Загрузка исходных данных из файлов"""
        try:
            with open(self.schedule_file, 'r', encoding='utf-8') as f:
                self.original_schedule = json.load(f)
            
            with open(self.preferences_file, 'r', encoding='utf-8') as f:
                self.preferences = json.load(f)
            
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
            if desired_teacher in teacher:
                return True
            if desired_parts[0] == teacher_words[0]:
                return True
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
        """Сохраняет расписание только если оно прошло валидацию"""
        try:
            is_valid = self.validator.validate_schedule(schedule_data)        
            if not is_valid:
                return False
            for i in range(10000):
                output_file_temp = output_file + f'{i}.csv'
                if not os.path.exists(output_file_temp):
                    output_file = output_file_temp
                    with open(output_file, 'w', encoding='utf-8', newline='') as f:
                        f.write(schedule_data.strip())
                    break
            print(f"Расписание успешно сохранено в {output_file}")
            return True
            
        except Exception as e:
            print(f"Ошибка при сохранении расписания: {e}")
            return False

    async def send_single_request(self, session: aiohttp.ClientSession, model_name: str, attempt ):
        """Асинхронная отправка одного запроса к API"""
        async with self.semaphore: 
            api_key = self._get_random_api_key()
            model_id = self._get_model_id(model_name)
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            
            data = {
                "model": model_id,
                "messages": [
                    {
                        "role": "system",
                        "content": """Ты - алгоритм генерации учебных расписаний. Твоя задача - создать одно оптимальное расписание без временных конфликтов, следуя строгим правилам.

**Алгоритм работы:**
1. Анализ входных данных:
   - Рассортируй предметы по приоритету: сначала предметы с наименьшим количеством групп
   - Для предметов с 1 или 2 группами - высокий приоретет 
   - Для предметов с 5+ группами и одной парой на группу - низкий приоритет
   - Для предметов с 5+ группами и одна пара очно и одна пара онлайн  - низкий приоритет
   - Для предметов с 5+ группами и двумя или более парами на группу - средний приоритет

2. Процесс составления расписания:
   a. Инициализируй пустое расписание и множество занятых временных слотов
   b. Для каждого предмета в порядке приоритета:
      1. Проанализируй все доступные группы предмета
      2. Выбери СЛУЧАЙНУЮ группу и проверь, что все пары которой:
          - Не пересекаются с занятыми временными слотами
          - Максимально заполняют свободные временные промежутки
      3. Добавь ВСЕ выбранные пары в расписание из группы  
      4. ЗАФИКСИРУЙ занятые временные слоты 
      5. ВЫВЕСТИ ВСЁ ЗАНЯТОЕ ВРЕМЯ
   с. Валидация расписания:
      1. Убедись, что для каждого предмета выбрана ровно одна группа
      2. ПРОВЕРЬ отсутствие временных конфликтов (день+время)
      3. Подтверди, что все пары выбранных групп включены
      4. ПОДТВЕРДИ, что ВСЕ параметры (день, время, преподаватель, аудитория, институт) у каждой пары верные  
   b. При обнаружении проблемы:
      1. Отменить последнее добавление
      2. Попробовать следующую подходящую группу
      3. Если варианты исчерпаны - вернуться еще на шаг назад

 
3. Валидация расписания:
   a. Проверь, что все исходные предметы присутствуют
   b. Убедись, что для каждого предмета выбрана ровно одна группа
   c. Проверь отсутствие временных конфликтов (день+время)
   d. Подтверди, что все пары выбранных групп включены

4. Обработка ошибок:
   При обнаружении проблемы:
     1. Отменить последнее добавление
     2. Попробовать следующую подходящую группу
     3. Если варианты исчерпаны - вернуться на шаг назад


**Формат входных данных (JSON):**
{
  "Предмет": {
    "Группа": [
      ["День", "Время", "Аудитория", "Преподаватель", "Институт"],
      ...
    ],
    ...
  },
  ...
}

**Требования к обработке:**
1. Для каждого предмета - ровно одна выбранная группа
2. Все пары выбранной группы должны быть включены
3. Строгий запрет временных пересечений (одинаковые день+время)
4. Проверка после каждого добавленного предмета
5. Онлайн пары тоже добавлять в расписание 
6. Создать ровано одно расписание 

**Формат вывода (CSV):**
"Day","Time","Auditory","Subject","Group","Teacher","Institute"
"Monday","08:30","Р101","Математика","АТ-07","Иванов Иван Иванович","Институт 1"

**Правила валидации:**
1. Все поля должны быть в кавычках
2. UTF-8 кодировка
3. Обязательные поля: Day, Time, Auditory, Subject, Group, Teacher, Institute

**Выводи все размышления, но после вывода CSV никаких дополнительных сообщений быть не должно. И Выводить только один вариант расписание.**
"""
                    },
                    {
                        "role": "user",
                        "content": json.dumps(self.filtered_schedule, ensure_ascii=False, indent=2)
                    }
                ],
                "temperature": 0.2,
            }

            try:
                print(f"Отправляем запрос к API с моделью {attempt}...")
                async with session.post(url, headers=headers, json=data) as response:
                    response.raise_for_status()
                    result = await response.json()
                    
                    if 'choices' in result and len(result['choices']) > 0:
                        schedule_data = result['choices'][0]['message']['content']
                        print(f"Получен ответ для модели {attempt}")
                        schedule_data = schedule_data[schedule_data.find('"Day'):]
                        print(schedule_data)
                        
                        output_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                                 'data', 'schedules', 'temp', 'schedule_variant_')
                        
                        if self.save_validated_schedule(schedule_data, output_file):
                            print(f"Расписание успешно сгенерировано и сохранено для модели {attempt}")
                            return True
                        else:
                            print(f"Расписание не прошло валидацию для модели {attempt}")
                            return False
                    else:
                        print(f"Неверный формат ответа от API для модели {attempt}")
                        return False
            except Exception as e:
                print(f"Ошибка при отправке сообщения для модели {attempt}: {str(e)}")
                return False

    def generate_schedule(self, model_name: str = "DeepSeek R1T") -> int:
        """
        Синхронный метод для генерации расписания.
        Возвращает количество успешно сгенерированных и сохраненных расписаний.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            self.load_data()
            self.filtered_schedule = self.original_schedule.copy()
            self.filter_by_undesired_time()
            self.filter_by_desired_groups()
            self.filter_by_undesired_institutes()

            if not self.check_subjects_have_groups():
                print("Ошибка: не все предметы имеют доступные группы после фильтрации")
                return 0

            async def run_requests():
                async with aiohttp.ClientSession() as session:
                    tasks = [self.send_single_request(session, model_name, i) for i in range(10)]
                    results = await asyncio.gather(*tasks, return_exceptions=False)
                    
                    success_count = 0
                    for result in results:
                        if result:
                            success_count += 1
                    print(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', f'Сгенерировано расписаний:{success_count}.txt'))
                    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', f'Сгенерировано расписаний {success_count}.txt'), 'w', encoding='utf-8') as f:
                        f.write(f'Макс гондон!!!!!!!!!!!!!!\nСгенерировано {success_count} расписаний!')
                    return success_count

            return loop.run_until_complete(run_requests())
        finally:
            loop.close()