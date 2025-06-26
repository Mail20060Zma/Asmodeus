import json
import random
import os
from typing import Dict, Any, Optional, List
import aiohttp
import asyncio
import requests
import time
from schedule_validator import ScheduleValidator

class APISender:
    def __init__(self):
        self.config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
        self.models_config = self._load_json('api_model.json')
        self.api_keys = self._load_json('api_keys.json')
        self.schedule_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'schedules', 'database', 'schedule.json')
        self.preferences_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'schedules', 'database', 'preferences.json')
        self.validator = ScheduleValidator()
        self.original_schedule: Dict = {}
        self.preferences: Dict = {}
        self.semaphore = asyncio.Semaphore(1000)
        self.api_keys_used = list
        
    def _load_json(self, filename: str) -> Dict[str, Any]:
        """Загрузка JSON файла из конфигурационной директории"""
        file_path =  os.path.join(self.config_dir, filename) 
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл конфигурации {filename} не найден в {self.config_dir}")
        except json.JSONDecodeError:
            raise ValueError(f"Ошибка в формате JSON файла {filename}")

    async def fetch_api_keys(self, n: int) -> list[str]:
        """Асинхронно получает N валидных API-ключей
        Возвращает список только валидных ключей"""
        async def _get_single_key(session: aiohttp.ClientSession, api_key: str) -> str | None:
            """Вложенная функция для получения одного ключа"""
            url = "https://openrouter.ai/api/v1/keys"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            try:
                async with session.post(url, headers=headers, json={"name": "name"}) as response:
                    response.raise_for_status()
                    data = await response.json()
                    data["p_api"] = api_key
                    return data
            except Exception as e:
                print(f"Ошибка при получении ключа {api_key}: {str(e)}")
                return None

        async with aiohttp.ClientSession() as session:
            tasks = [_get_single_key(session, random.choice(self.api_keys)) for _ in range(n)]
            results = await asyncio.gather(*tasks)
            return results

    def _get_model_id(self, model_name: Optional[str] = None) -> str:
        """Получение ID модели"""
        if model_name is None:
            model_name = self.models_config.get('default_model')
        
        model_id = self.models_config[model_name]
        if not model_id:
            raise ValueError(f"Модель {model_name} не найдена в конфигурации")
        
        return model_id


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
    
    def filter_by_single_group_conflicts(self) -> None:
        """Фильтрация групп других предметов, которые конфликтуют по времени с предметами,
        у которых осталась только одна группа после всех предыдущих фильтраций."""
        single_group_subjects = {
            subject: groups 
            for subject, groups in self.filtered_schedule.items() 
            if len(groups) == 1
        }

        if not single_group_subjects:
            return

        mandatory_slots = set()
        for subject, groups in single_group_subjects.items():
            group_name = next(iter(groups))
            for lesson in groups[group_name]:
                day = lesson[0]
                time = lesson[1]
                mandatory_slots.add((day, time))

        for subject in list(self.filtered_schedule.keys()):
            if subject in single_group_subjects:
                continue

            for group in list(self.filtered_schedule[subject].keys()):
                lessons = self.filtered_schedule[subject][group]
                for lesson in lessons:
                    day = lesson[0]
                    time = lesson[1]
                    if (day, time) in mandatory_slots:
                        del self.filtered_schedule[subject][group]
                        break

    def check_subjects_have_groups(self) -> bool:
        """Проверка наличия хотя бы одной группы для каждого предмета 
        и базовой возможности составления расписания без явных конфликтов"""
        return True
        if not all(len(groups) > 0 for groups in self.filtered_schedule.values()):
            print("Ошибка: не все предметы имеют доступные группы после фильтрации")
            return False
        
        all_time_slots = []
        for subject, groups in self.filtered_schedule.items():
            subject_slots = set()
            for group_info in groups.values():
                for lesson in group_info:
                    day = lesson[0]
                    time = lesson[1]
                    subject_slots.add((day, time))
            all_time_slots.append(subject_slots)
        
        for i, slots in enumerate(all_time_slots):
            other_slots = set()
            for j, other in enumerate(all_time_slots):
                if i != j:
                    other_slots.update(other)
            
            if slots and all(slot in other_slots for slot in slots):
                print(f"Предупреждение: все временные слоты для предмета {list(self.filtered_schedule.keys())[i]} "
                    f"пересекаются с другими предметами")
                return False
        
        return True

    def save_validated_schedule(self, schedule_data: str, output_file: str) -> bool:
        """Сохраняет расписание только если оно прошло валидацию"""
        try:
            is_valid = self.validator.validate_schedule(schedule_data)        
            if not is_valid:
                return False
            for i in range(100):
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

    async def send_single_request(self, session: aiohttp.ClientSession, model_name: str, attempt, promt_users: str):
        """Асинхронная отправка одного запроса к API"""
        async with self.semaphore: 
            api_key = self.api_keys_used[attempt]["key"] # type: ignore
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
                        "content": """Ты - алгоритм генерации учебных расписаний. Твоя задача - создать одно оптимальное расписание без временных конфликтов, следуя строгим правилам. Максимально подробно расписывай все свои действия до мельчайших деталей.

**Алгоритм работы:**
1. Анализ входных данных:
    - Рассортируй предметы по приоритету: 
    - Для предметов с 1 или 2 группами - высокий приоретет 
    - Для предметов с пятью или более группами и двумя или более парами на группу - средний приоритет
    - Для предметов с пятью или более группами и одной парой на группу - низкий приоритет
    - Для предметов с пятью или более группами и одна пара очно и одна пара онлайн  - низкий приоритет
    - Также учитывать предпочтения пользователей если такие имеются (путем удаление всех групп где есть пары которые противоречат предпочтениям

2. Процесс составления расписания:
    a. Инициализируй пустое расписание и множество занятых временных слотов
    b. Для каждого предмета в порядке приоритета:
        1. Проанализируй все доступные группы предмета
        2. Выбери СЛУЧАЙНУЮ группу после проверь (ИСКАТЬ ГРУППУ ДО ТЕХ ПОР ПОКА ГРУППЫ НЕ КОНЧАТЬСЯ):
            - Что пары из этой группы не пересекаются с занятыми временными слотами
            - Максимально заполняют свободные временные промежутки
            - если группа удовлетворяет всем условиям то тогда ее добавляем все пары из этой группы, если нет берем следуйшие случайную группу
        3. ЗАФИКСИРУЙ занятые временные слоты 
        4. ВЫВЕСТИ ВСЁ множество занятых временных слотов
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

**Выводи все размышления, но после вывода CSV никаких дополнительных сообщений быть не должно.И Выводить только один вариант расписание.**
"""
                    },
                    {
                        "role": "user",
                        "content": f"{promt_users}\n" + json.dumps(self.filtered_schedule, ensure_ascii=False, indent=2)
                    }
                ],
                "temperature": 0.22,
            }
            
            try:
                print(f"Отправляем запрос к API с моделью {attempt}...")
                async with asyncio.timeout(300):
                    async with session.post(url, headers=headers, json=data) as response:
                        response.raise_for_status()
                        result = await response.json()
                        if 'choices' in result and len(result['choices']) > 0:
                            schedule_data = result['choices'][0]['message']['content']
                            print(f"Получен ответ для модели {attempt}")
                            
                            schedule_data = schedule_data[schedule_data.find('"Day'):schedule_data.rfind("```") if schedule_data.rfind("```") else None]
                            print(schedule_data)
                            output_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                                    'data', 'schedules', 'ready', 'schedule_variant_')
                            is_valid = self.save_validated_schedule(schedule_data, output_file)
                            if is_valid:
                                print(f"Расписание успешно сгенерировано и сохранено для модели {attempt}")
                                return True
                            else:
                                print(f"Расписание не прошло валидацию для модели {attempt}")
                                return False
                        else:
                            print(f"Неверный формат ответа от API для модели {attempt}")
                            return False
            except asyncio.TimeoutError:
                is_valid = False
                print(f"Превышено время ожидания (300 сек) для модели {attempt}")
                return False
            except Exception as e:
                is_valid = False
                print(f"Ошибка при отправке сообщения для модели {attempt}: {str(e)}")
                return False
            finally:
                response_del = requests.delete("https://openrouter.ai/api/v1/keys/" + self.api_keys_used[attempt]['data']['hash'],
                                                headers = {"Authorization": f"Bearer {self.api_keys_used[attempt]["p_api"]}"}) # type: ignore 
                print(response_del.json())
                with open(os.path.join(self.config_dir, 'schedules_ready', f'{is_valid} {attempt}.txt'), 'w', encoding='utf-8') as f:
                    f.write(f"{is_valid}")

    def generate_schedule(self, model_name: str = "DeepSeek R1T", promt_users:str = '', attempt: int = 10, ) -> int:
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
            self.filter_by_single_group_conflicts()
            self.sort_subjects_by_groups_count()
            print(json.dumps(self.filtered_schedule, ensure_ascii=False, indent=2))

            if not self.check_subjects_have_groups():
                with open(os.path.join(self.config_dir, 'schedules_ready', f'error.txt'), 'w', encoding='utf-8') as f:
                    f.write(f'error')
                return 0
            
            self.api_keys_used = loop.run_until_complete(self.fetch_api_keys(attempt))
            print(f"Сгенерировано {len(self.api_keys_used)} ключей!\nЖдем 10 секунд!")
            time.sleep(10)

            async def run_requests():
                async with aiohttp.ClientSession() as session:
                    tasks = [self.send_single_request(session, model_name, i, promt_users) for i in range(attempt)]
                    results = await asyncio.gather(*tasks, return_exceptions=False)
                    return
            return loop.run_until_complete(run_requests())
        finally:
            success_count = sum("True" in f for f in os.listdir(os.path.join(self.config_dir, 'schedules_ready')))
            print(f"Успешно сгенерировано расписаний: {success_count}")
            loop.close()

def main():
    sender = APISender()
        #                0              1               2              3              4               5              6                  7               8               9                       10   
    model_name = ["Kimi Dev", "Qwen3-235B-A22B", "Qwen2.5-72B", "DeepSeek V3", "DeepSeek R1", "DeepSeek R1T", "Gemini 2", "Llama 4 Scout",  "MAI DS R1", "NVIDIA: Llama 3.3", "Deepseek R1 Qwen3 8B"][5]
    promt_users = ""
    try:
        model_name_file = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config',))
        for file in model_name_file:
            if "model_name" in file:
                model_name = file[file.find(" ")+1:file.rfind(".")]
                print(model_name)
                print(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', file))
                os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', file))

            if "promt_users" in file:
                promt_users = file[file.find(" ")+1:file.rfind(".")]
                print(promt_users)
                print(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', file))
                os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', file))
    finally:
        sender.generate_schedule(model_name, promt_users)
        return 

if __name__ == "__main__":
    time.sleep(5)
    main()