import pygame
import sys
from collections import defaultdict
from asmo_UI import *
from ai_generate_validator import *
from schedule_converter_interface import *
import json
import time

FPS = 60

pygame.init()

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'schedules_ready'), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'schedules', 'ready'), exist_ok=True)

SIZE = [1350, 800]
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Asmodeus v.0.7.0')
clock = pygame.time.Clock()
programIcon = pygame.image.load(os.path.join(root_path, 'assets', 'icon2.png'))
pygame.display.set_icon(programIcon)

def play_sound(file_path):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_path)
    sound.play()

is_mouse_clicked = False
is_long_click = False

MAIN_SUBJECT_PULL = csv_to_schedule_dict(os.path.join(root_path, 'data', 'schedules', 'database', 'schedule.csv'))

ai_pull = []
ai_models_dict = json.load(open(os.path.join(root_path, "src", "config", "api_model.json"))).items()
for ai_model_list, ai_model_full in ai_models_dict:
    ai_model_full = ai_model_full[:ai_model_full.find(":")]
    ai_model_full = ai_model_full.replace("/", "-")
    if len(ai_model_full)>15:
        ai_model_full = ai_model_full[:15] + "/" + ai_model_full[15:30]
    ai_pull.append(Drop_menu_subject(ai_model_full, ai_model_list, '', gap_size=20))
ai_pull.insert(0, Drop_menu_subject('AsmoAI(no text)', 'AsmoAI', '', gap_size=20))

teacher_group_new_desires = []

settings = {}
with open(r'config\config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            settings['AsmoAI_warning'] = data['AsmoAI_warning']
            settings['TextPrompt_warning'] = data['TextPrompt_warning']
            settings['NoPrompt_warning'] = data['NoPrompt_warning']

def teacher_group_add_new_desire():
    global teacher_group_new_desires
    new_desire = [ai_full_subject.return_system_name_selected(), ai_full_teacher_group_subject.return_main_name_selected()]
    if new_desire not in teacher_group_new_desires and None not in new_desire:
        teacher_group_new_desires.append(new_desire)

table_top_text = Text(screen, SMALL_FONT, [50,10], '   Понедельник           Вторник             Среда             Четверг            Пятница            Суббота')

mond1 = Drop_menu(screen, 'mond1', [50,50], [200,100], MAIN_SUBJECT_PULL['Monday']['08:30'])
mond2 = Drop_menu(screen, 'mond2', [50,160], [200,100], MAIN_SUBJECT_PULL['Monday']['10:15'])
mond3 = Drop_menu(screen, 'mond3', [50,270], [200,100], MAIN_SUBJECT_PULL['Monday']['12:00'])
mond4 = Drop_menu(screen, 'mond4', [50,380], [200,100], MAIN_SUBJECT_PULL['Monday']['14:15'])
mond5 = Drop_menu(screen, 'mond5', [50,490], [200,100], MAIN_SUBJECT_PULL['Monday']['16:00'])
mond6 = Drop_menu(screen, 'mond6', [50,600], [200,100], MAIN_SUBJECT_PULL['Monday']['17:40'])

tues1 = Drop_menu(screen, 'tues1', [260,50], [200,100], MAIN_SUBJECT_PULL['Tuesday']['08:30'])
tues2 = Drop_menu(screen, 'tues2', [260,160], [200,100], MAIN_SUBJECT_PULL['Tuesday']['10:15'])
tues3 = Drop_menu(screen, 'tues3', [260,270], [200,100], MAIN_SUBJECT_PULL['Tuesday']['12:00'])
tues4 = Drop_menu(screen, 'tues4', [260,380], [200,100], MAIN_SUBJECT_PULL['Tuesday']['14:15'])
tues5 = Drop_menu(screen, 'tues5', [260,490], [200,100], MAIN_SUBJECT_PULL['Tuesday']['16:00'])
tues6 = Drop_menu(screen, 'tues6', [260,600], [200,100], MAIN_SUBJECT_PULL['Tuesday']['17:40'])

wedn1 = Drop_menu(screen, 'wedn1', [470,50], [200,100], MAIN_SUBJECT_PULL['Wednesday']['08:30'])
wedn2 = Drop_menu(screen, 'wedn2', [470,160], [200,100], MAIN_SUBJECT_PULL['Wednesday']['10:15'])
wedn3 = Drop_menu(screen, 'wedn3', [470,270], [200,100], MAIN_SUBJECT_PULL['Wednesday']['12:00'])
wedn4 = Drop_menu(screen, 'wedn4', [470,380], [200,100], MAIN_SUBJECT_PULL['Wednesday']['14:15'])
wedn5 = Drop_menu(screen, 'wedn5', [470,490], [200,100], MAIN_SUBJECT_PULL['Wednesday']['16:00'])
wedn6 = Drop_menu(screen, 'wedn6', [470,600], [200,100], MAIN_SUBJECT_PULL['Wednesday']['17:40'])

thur1 = Drop_menu(screen, 'thur1', [680,50], [200,100], MAIN_SUBJECT_PULL['Thursday']['08:30'])
thur2 = Drop_menu(screen, 'thur2', [680,160], [200,100], MAIN_SUBJECT_PULL['Thursday']['10:15'])
thur3 = Drop_menu(screen, 'thur3', [680,270], [200,100], MAIN_SUBJECT_PULL['Thursday']['12:00'])
thur4 = Drop_menu(screen, 'thur4', [680,380], [200,100], MAIN_SUBJECT_PULL['Thursday']['14:15'])
thur5 = Drop_menu(screen, 'thur5', [680,490], [200,100], MAIN_SUBJECT_PULL['Thursday']['16:00'])
thur6 = Drop_menu(screen, 'thur6', [680,600], [200,100], MAIN_SUBJECT_PULL['Thursday']['17:40'])

frid1 = Drop_menu(screen, 'frid1', [890,50], [200,100], MAIN_SUBJECT_PULL['Friday']['08:30'])
frid2 = Drop_menu(screen, 'frid2', [890,160], [200,100], MAIN_SUBJECT_PULL['Friday']['10:15'])
frid3 = Drop_menu(screen, 'frid3', [890,270], [200,100], MAIN_SUBJECT_PULL['Friday']['12:00'])
frid4 = Drop_menu(screen, 'frid4', [890,380], [200,100], MAIN_SUBJECT_PULL['Friday']['14:15'])
frid5 = Drop_menu(screen, 'frid5', [890,490], [200,100], MAIN_SUBJECT_PULL['Friday']['16:00'])
frid6 = Drop_menu(screen, 'frid6', [890,600], [200,100], MAIN_SUBJECT_PULL['Friday']['17:40'])

satu1 = Drop_menu(screen, 'satu1', [1100,50], [200,100], MAIN_SUBJECT_PULL['Saturday']['08:30'])
satu2 = Drop_menu(screen, 'satu2', [1100,160], [200,100], MAIN_SUBJECT_PULL['Saturday']['10:15'])
satu3 = Drop_menu(screen, 'satu3', [1100,270], [200,100], MAIN_SUBJECT_PULL['Saturday']['12:00'])
satu4 = Drop_menu(screen, 'satu4', [1100,380], [200,100], MAIN_SUBJECT_PULL['Saturday']['14:15'])
satu5 = Drop_menu(screen, 'satu5', [1100,490], [200,100], MAIN_SUBJECT_PULL['Saturday']['16:00'])
satu6 = Drop_menu(screen, 'satu6', [1100,600], [200,100], MAIN_SUBJECT_PULL['Saturday']['17:40'])

clear_message_text = Text(screen, MAIN_FONT, [10,0], 'Вы уверены?')
clear_message_yes = Button(screen, [10, 90], [70, 50], SMALL_FONT, 'ДА')
clear_message_no = Button(screen, [160, 90], [70, 50], SMALL_FONT, 'Нет')
clear_message = Message_window(screen, [240, 150], [clear_message_text, clear_message_no, clear_message_yes])

offset = 270
ai_generate_button = Button(screen, [50, 720], [400, 60], text = 'Сгенерировать с ИИ')
scedule_number_text = Text(screen, MAIN_FONT, [500 + offset, 720], 'Номер расписания:')
scedule_actual_number_text = Text(screen, MAIN_FONT, [919 + offset, 720], '01')
scedule_back_button = Button(screen, [840 + offset, 720], [60, 60], text='<')
scedule_next_button = Button(screen, [970 + offset, 720], [60, 60], text='>')

ai_message_text_model = Text(screen, SMALL_FONT, [10,20], 'Агент генерации: ')
ai_message_choice_model = Drop_menu(screen, 'ai_choice', [210, 10], [190, 50], ai_pull)
ai_message_prompt_switch_text = Text(screen, SMALL_FONT, [10, 75], 'Доп.Промпт: ')
ai_message_prompt_switch = Switch(screen, [150, 75], already_on=True)
ai_message_prompt_more_button = Button(screen, [220, 75], [160, 30], SMALL_FONT, 'Больше опций')
ai_message_prompt_text = Text(screen, SMALL_FONT, [10, 130], 'Промпт: ')
ai_message_prompt = Input_field(screen, [100, 130], 300, 40, font=SMALL_FONT, text="")
ai_message_cancel_button = Button(screen, [10, 200], [150, 50], text='Отмена')
ai_message_start_button = Button(screen, [180, 200], [220, 50], text='Старт', rainbow_highlight=True)

ai_message = Message_window(screen, [410, 270], [ai_message_text_model,
                                                 ai_message_prompt_switch_text,
                                                 ai_message_prompt_switch,
                                                 ai_message_prompt_text,
                                                 ai_message_prompt,
                                                 ai_message_cancel_button,
                                                 ai_message_start_button,
                                                 ai_message_prompt_more_button,
                                                 ai_message_choice_model])

mond_ai_more_message_title = Text(screen, SMALL_FONT, [10, 5], 'Выбор дней и пар:')
mond_ai_more_message_prev_day_button = Button(screen, [290, 5], [30, 30], SMALL_FONT, '<')
mond_ai_more_message_next_day_button = Button(screen, [460, 5], [30, 30], SMALL_FONT, '>')
mond_ai_more_message_mond_text = Text(screen, SMALL_FONT, [333, 5], 'Понедельник')
mond_ai_more_message_time_text1 = Text(screen, SMALL_FONT, [10, 70], '8:30-10:00               14:15-15:45')
mond_ai_more_message_time_text2 = Text(screen, SMALL_FONT, [10, 110], '10:15-11:45              16:00-17:30')
mond_ai_more_message_time_text3 = Text(screen, SMALL_FONT, [10, 150], '12:00-13:30              17:40-19:10')
mond_ai_more_message_time_switch_8_30 = Switch(screen, [150, 70], already_on=True)
mond_ai_more_message_time_switch_10_15 = Switch(screen, [150, 110], already_on=True)
mond_ai_more_message_time_switch_12_00 = Switch(screen, [150, 150], already_on=True)
mond_ai_more_message_time_switch_14_15 = Switch(screen, [430, 70], already_on=True)
mond_ai_more_message_time_switch_16_00 = Switch(screen, [430, 110], already_on=True)
mond_ai_more_message_time_switch_17_40 = Switch(screen, [430, 150], already_on=True)
mond_ai_more_message_back_button = Button(screen, [370, 260], [120,30], SMALL_FONT, 'Сохранить')
mond_ai_more_message_drop_button = Button(screen, [240, 260], [120,30], SMALL_FONT, 'Сбросить')
mond_ai_more_message_prev_button = Button(screen, [10, 260], [30, 30], SMALL_FONT, '<')
mond_ai_more_message_next_button = Button(screen, [50, 260], [30, 30], SMALL_FONT, '>')
mond_ai_more_message = Message_window(screen, [500,300], [mond_ai_more_message_title,
                                                     mond_ai_more_message_mond_text,
                                                     mond_ai_more_message_prev_day_button,
                                                     mond_ai_more_message_next_day_button,
                                                     mond_ai_more_message_time_text1,
                                                     mond_ai_more_message_time_text2,
                                                     mond_ai_more_message_time_text3,
                                                     mond_ai_more_message_time_switch_8_30, mond_ai_more_message_time_switch_14_15,
                                                     mond_ai_more_message_time_switch_10_15, mond_ai_more_message_time_switch_16_00,
                                                     mond_ai_more_message_time_switch_12_00, mond_ai_more_message_time_switch_17_40,
                                                     mond_ai_more_message_back_button,
                                                     mond_ai_more_message_drop_button,
                                                     mond_ai_more_message_prev_button,
                                                     mond_ai_more_message_next_button])

tues_ai_more_message_title = Text(screen, SMALL_FONT, [10, 5], 'Выбор дней и пар:')
tues_ai_more_message_prev_day_button = Button(screen, [290, 5], [30, 30], SMALL_FONT, '<')
tues_ai_more_message_next_day_button = Button(screen, [460, 5], [30, 30], SMALL_FONT, '>')
tues_ai_more_message_tues_text = Text(screen, SMALL_FONT, [333, 5], '  Вторник')
tues_ai_more_message_time_text1 = Text(screen, SMALL_FONT, [10, 70], '8:30-10:00               14:15-15:45')
tues_ai_more_message_time_text2 = Text(screen, SMALL_FONT, [10, 110], '10:15-11:45              16:00-17:30')
tues_ai_more_message_time_text3 = Text(screen, SMALL_FONT, [10, 150], '12:00-13:30              17:40-19:10')
tues_ai_more_message_time_switch_8_30 = Switch(screen, [150, 70], already_on=True)
tues_ai_more_message_time_switch_10_15 = Switch(screen, [150, 110], already_on=True)
tues_ai_more_message_time_switch_12_00 = Switch(screen, [150, 150], already_on=True)
tues_ai_more_message_time_switch_14_15 = Switch(screen, [430, 70], already_on=True)
tues_ai_more_message_time_switch_16_00 = Switch(screen, [430, 110], already_on=True)
tues_ai_more_message_time_switch_17_40 = Switch(screen, [430, 150], already_on=True)
tues_ai_more_message_back_button = Button(screen, [370, 260], [120,30], SMALL_FONT, 'Сохранить')
tues_ai_more_message_drop_button = Button(screen, [240, 260], [120,30], SMALL_FONT, 'Сбросить')
tues_ai_more_message_prev_button = Button(screen, [10, 260], [30, 30], SMALL_FONT, '<')
tues_ai_more_message_next_button = Button(screen, [50, 260], [30, 30], SMALL_FONT, '>')
tues_ai_more_message = Message_window(screen, [500,300], [tues_ai_more_message_title,
                                                     tues_ai_more_message_tues_text,
                                                     tues_ai_more_message_prev_day_button,
                                                     tues_ai_more_message_next_day_button,
                                                     tues_ai_more_message_time_text1,
                                                     tues_ai_more_message_time_text2,
                                                     tues_ai_more_message_time_text3,
                                                     tues_ai_more_message_time_switch_8_30, tues_ai_more_message_time_switch_14_15,
                                                     tues_ai_more_message_time_switch_10_15, tues_ai_more_message_time_switch_16_00,
                                                     tues_ai_more_message_time_switch_12_00, tues_ai_more_message_time_switch_17_40,
                                                     tues_ai_more_message_back_button,
                                                     tues_ai_more_message_drop_button,
                                                     tues_ai_more_message_prev_button,
                                                     tues_ai_more_message_next_button])

wedn_ai_more_message_title = Text(screen, SMALL_FONT, [10, 5], 'Выбор дней и пар:')
wedn_ai_more_message_prev_day_button = Button(screen, [290, 5], [30, 30], SMALL_FONT, '<')
wedn_ai_more_message_next_day_button = Button(screen, [460, 5], [30, 30], SMALL_FONT, '>')
wedn_ai_more_message_wedn_text = Text(screen, SMALL_FONT, [333, 5], '   Среда')
wedn_ai_more_message_time_text1 = Text(screen, SMALL_FONT, [10, 70], '8:30-10:00               14:15-15:45')
wedn_ai_more_message_time_text2 = Text(screen, SMALL_FONT, [10, 110], '10:15-11:45              16:00-17:30')
wedn_ai_more_message_time_text3 = Text(screen, SMALL_FONT, [10, 150], '12:00-13:30              17:40-19:10')
wedn_ai_more_message_time_switch_8_30 = Switch(screen, [150, 70], already_on=True)
wedn_ai_more_message_time_switch_10_15 = Switch(screen, [150, 110], already_on=True)
wedn_ai_more_message_time_switch_12_00 = Switch(screen, [150, 150], already_on=True)
wedn_ai_more_message_time_switch_14_15 = Switch(screen, [430, 70], already_on=True)
wedn_ai_more_message_time_switch_16_00 = Switch(screen, [430, 110], already_on=True)
wedn_ai_more_message_time_switch_17_40 = Switch(screen, [430, 150], already_on=True)
wedn_ai_more_message_back_button = Button(screen, [370, 260], [120,30], SMALL_FONT, 'Сохранить')
wedn_ai_more_message_drop_button = Button(screen, [240, 260], [120,30], SMALL_FONT, 'Сбросить')
wedn_ai_more_message_prev_button = Button(screen, [10, 260], [30, 30], SMALL_FONT, '<')
wedn_ai_more_message_next_button = Button(screen, [50, 260], [30, 30], SMALL_FONT, '>')
wedn_ai_more_message = Message_window(screen, [500,300], [wedn_ai_more_message_title,
                                                     wedn_ai_more_message_wedn_text,
                                                     wedn_ai_more_message_prev_day_button,
                                                     wedn_ai_more_message_next_day_button,
                                                     wedn_ai_more_message_time_text1,
                                                     wedn_ai_more_message_time_text2,
                                                     wedn_ai_more_message_time_text3,
                                                     wedn_ai_more_message_time_switch_8_30, wedn_ai_more_message_time_switch_14_15,
                                                     wedn_ai_more_message_time_switch_10_15, wedn_ai_more_message_time_switch_16_00,
                                                     wedn_ai_more_message_time_switch_12_00, wedn_ai_more_message_time_switch_17_40,
                                                     wedn_ai_more_message_back_button,
                                                     wedn_ai_more_message_drop_button,
                                                     wedn_ai_more_message_prev_button,
                                                     wedn_ai_more_message_next_button])

thur_ai_more_message_title = Text(screen, SMALL_FONT, [10, 5], 'Выбор дней и пар:')
thur_ai_more_message_prev_day_button = Button(screen, [290, 5], [30, 30], SMALL_FONT, '<')
thur_ai_more_message_next_day_button = Button(screen, [460, 5], [30, 30], SMALL_FONT, '>')
thur_ai_more_message_thur_text = Text(screen, SMALL_FONT, [333, 5], '  Четверг')
thur_ai_more_message_time_text1 = Text(screen, SMALL_FONT, [10, 70], '8:30-10:00               14:15-15:45')
thur_ai_more_message_time_text2 = Text(screen, SMALL_FONT, [10, 110], '10:15-11:45              16:00-17:30')
thur_ai_more_message_time_text3 = Text(screen, SMALL_FONT, [10, 150], '12:00-13:30              17:40-19:10')
thur_ai_more_message_time_switch_8_30 = Switch(screen, [150, 70], already_on=True)
thur_ai_more_message_time_switch_10_15 = Switch(screen, [150, 110], already_on=True)
thur_ai_more_message_time_switch_12_00 = Switch(screen, [150, 150], already_on=True)
thur_ai_more_message_time_switch_14_15 = Switch(screen, [430, 70], already_on=True)
thur_ai_more_message_time_switch_16_00 = Switch(screen, [430, 110], already_on=True)
thur_ai_more_message_time_switch_17_40 = Switch(screen, [430, 150], already_on=True)
thur_ai_more_message_back_button = Button(screen, [370, 260], [120,30], SMALL_FONT, 'Сохранить')
thur_ai_more_message_drop_button = Button(screen, [240, 260], [120,30], SMALL_FONT, 'Сбросить')
thur_ai_more_message_prev_button = Button(screen, [10, 260], [30, 30], SMALL_FONT, '<')
thur_ai_more_message_next_button = Button(screen, [50, 260], [30, 30], SMALL_FONT, '>')
thur_ai_more_message = Message_window(screen, [500,300], [thur_ai_more_message_title,
                                                     thur_ai_more_message_thur_text,
                                                     thur_ai_more_message_prev_day_button,
                                                     thur_ai_more_message_next_day_button,
                                                     thur_ai_more_message_time_text1,
                                                     thur_ai_more_message_time_text2,
                                                     thur_ai_more_message_time_text3,
                                                     thur_ai_more_message_time_switch_8_30, thur_ai_more_message_time_switch_14_15,
                                                     thur_ai_more_message_time_switch_10_15, thur_ai_more_message_time_switch_16_00,
                                                     thur_ai_more_message_time_switch_12_00, thur_ai_more_message_time_switch_17_40,
                                                     thur_ai_more_message_back_button,
                                                     thur_ai_more_message_drop_button,
                                                     thur_ai_more_message_prev_button,
                                                     thur_ai_more_message_next_button])

frid_ai_more_message_title = Text(screen, SMALL_FONT, [10, 5], 'Выбор дней и пар:')
frid_ai_more_message_prev_day_button = Button(screen, [290, 5], [30, 30], SMALL_FONT, '<')
frid_ai_more_message_next_day_button = Button(screen, [460, 5], [30, 30], SMALL_FONT, '>')
frid_ai_more_message_frid_text = Text(screen, SMALL_FONT, [333, 5], '  Пятница')
frid_ai_more_message_time_text1 = Text(screen, SMALL_FONT, [10, 70], '8:30-10:00               14:15-15:45')
frid_ai_more_message_time_text2 = Text(screen, SMALL_FONT, [10, 110], '10:15-11:45              16:00-17:30')
frid_ai_more_message_time_text3 = Text(screen, SMALL_FONT, [10, 150], '12:00-13:30              17:40-19:10')
frid_ai_more_message_time_switch_8_30 = Switch(screen, [150, 70], already_on=True)
frid_ai_more_message_time_switch_10_15 = Switch(screen, [150, 110], already_on=True)
frid_ai_more_message_time_switch_12_00 = Switch(screen, [150, 150], already_on=True)
frid_ai_more_message_time_switch_14_15 = Switch(screen, [430, 70], already_on=True)
frid_ai_more_message_time_switch_16_00 = Switch(screen, [430, 110], already_on=True)
frid_ai_more_message_time_switch_17_40 = Switch(screen, [430, 150], already_on=True)
frid_ai_more_message_back_button = Button(screen, [370, 260], [120,30], SMALL_FONT, 'Сохранить')
frid_ai_more_message_drop_button = Button(screen, [240, 260], [120,30], SMALL_FONT, 'Сбросить')
frid_ai_more_message_prev_button = Button(screen, [10, 260], [30, 30], SMALL_FONT, '<')
frid_ai_more_message_next_button = Button(screen, [50, 260], [30, 30], SMALL_FONT, '>')
frid_ai_more_message = Message_window(screen, [500,300], [frid_ai_more_message_title,
                                                     frid_ai_more_message_frid_text,
                                                     frid_ai_more_message_prev_day_button,
                                                     frid_ai_more_message_next_day_button,
                                                     frid_ai_more_message_time_text1,
                                                     frid_ai_more_message_time_text2,
                                                     frid_ai_more_message_time_text3,
                                                     frid_ai_more_message_time_switch_8_30, frid_ai_more_message_time_switch_14_15,
                                                     frid_ai_more_message_time_switch_10_15, frid_ai_more_message_time_switch_16_00,
                                                     frid_ai_more_message_time_switch_12_00, frid_ai_more_message_time_switch_17_40,
                                                     frid_ai_more_message_back_button,
                                                     frid_ai_more_message_drop_button,
                                                     frid_ai_more_message_prev_button,
                                                     frid_ai_more_message_next_button])

satu_ai_more_message_title = Text(screen, SMALL_FONT, [10, 5], 'Выбор дней и пар:')
satu_ai_more_message_prev_day_button = Button(screen, [290, 5], [30, 30], SMALL_FONT, '<')
satu_ai_more_message_next_day_button = Button(screen, [460, 5], [30, 30], SMALL_FONT, '>')
satu_ai_more_message_satu_text = Text(screen, SMALL_FONT, [333, 5], '  Суббота')
satu_ai_more_message_time_text1 = Text(screen, SMALL_FONT, [10, 70], '8:30-10:00               14:15-15:45')
satu_ai_more_message_time_text2 = Text(screen, SMALL_FONT, [10, 110], '10:15-11:45              16:00-17:30')
satu_ai_more_message_time_text3 = Text(screen, SMALL_FONT, [10, 150], '12:00-13:30              17:40-19:10')
satu_ai_more_message_time_switch_8_30 = Switch(screen, [150, 70], already_on=True)
satu_ai_more_message_time_switch_10_15 = Switch(screen, [150, 110], already_on=True)
satu_ai_more_message_time_switch_12_00 = Switch(screen, [150, 150], already_on=True)
satu_ai_more_message_time_switch_14_15 = Switch(screen, [430, 70], already_on=True)
satu_ai_more_message_time_switch_16_00 = Switch(screen, [430, 110], already_on=True)
satu_ai_more_message_time_switch_17_40 = Switch(screen, [430, 150], already_on=True)
satu_ai_more_message_back_button = Button(screen, [370, 260], [120,30], SMALL_FONT, 'Сохранить')
satu_ai_more_message_drop_button = Button(screen, [240, 260], [120,30], SMALL_FONT, 'Сбросить')
satu_ai_more_message_prev_button = Button(screen, [10, 260], [30, 30], SMALL_FONT, '<')
satu_ai_more_message_next_button = Button(screen, [50, 260], [30, 30], SMALL_FONT, '>')
satu_ai_more_message = Message_window(screen, [500,300], [satu_ai_more_message_title,
                                                     satu_ai_more_message_satu_text,
                                                     satu_ai_more_message_prev_day_button,
                                                     satu_ai_more_message_next_day_button,
                                                     satu_ai_more_message_time_text1,
                                                     satu_ai_more_message_time_text2,
                                                     satu_ai_more_message_time_text3,
                                                     satu_ai_more_message_time_switch_8_30, satu_ai_more_message_time_switch_14_15,
                                                     satu_ai_more_message_time_switch_10_15, satu_ai_more_message_time_switch_16_00,
                                                     satu_ai_more_message_time_switch_12_00, satu_ai_more_message_time_switch_17_40,
                                                     satu_ai_more_message_back_button,
                                                     satu_ai_more_message_drop_button,
                                                     satu_ai_more_message_prev_button,
                                                     satu_ai_more_message_next_button])

ai_more_message_title1 = Text(screen, SMALL_FONT, [10, 5], 'Выбор предметов, групп и преподавателей:')
ai_full_subject = Drop_menu(screen, 'ai_all_subject', [30,40], [200,100], MAIN_SUBJECT_PULL['All_subject'], selected_index=3)
ai_full_teacher_group_subject = Drop_menu(screen, 'ai_all_info_subject', [270,40], [200,100], MAIN_SUBJECT_PULL['Дополнительные главы математики. ИРИТ-РТФ (09 УГН)'])
ai_full_teacher_group_add_button = Button(screen, [190, 150], [120, 30], SMALL_FONT, 'Добавить')
ai_full_teacher_group_add_text = Text(screen, SMALL_FONT, [125, 190], f'Параметров добавлено: {len(teacher_group_new_desires)}')
ai_more_message_back_button1 = Button(screen, [370, 260], [120,30], SMALL_FONT, 'Сохранить')
ai_more_message_drop_button1 = Button(screen, [240, 260], [120,30], SMALL_FONT, 'Сбросить')
ai_more_message_prev_button1 = Button(screen, [10, 260], [30, 30], SMALL_FONT, '<')
ai_more_message_next_button1 = Button(screen, [50, 260], [30, 30], SMALL_FONT, '>')
ai_more_message1 = Message_window(screen, [500,300], [ai_more_message_title1,
                                                        ai_full_teacher_group_add_button,
                                                        ai_full_teacher_group_add_text,
                                                        ai_more_message_back_button1,
                                                        ai_more_message_drop_button1,
                                                        ai_more_message_prev_button1,
                                                        ai_more_message_next_button1,
                                                        ai_full_subject,
                                                        ai_full_teacher_group_subject])

generator_error_message_text1 = Text(screen, SMALL_FONT, [10, 10], 'ОШИБКА:')
generator_error_message_text2 = Text(screen, SMALL_FONT, [10, 50], '')
generator_error_message_ok_button = Button(screen, [290, 90], [100, 50], SMALL_FONT, 'OK')

generator_error_message = Message_window(screen, [400, 150], [generator_error_message_text1,
                                                              generator_error_message_text2, 
                                                              generator_error_message_ok_button])

generator_warning_message_text1 = Text(screen, SMALL_FONT, [10, 10], 'Предупреждение:')
generator_warning_message_text2 = Long_Text(screen, SMALL_FONT, [10, 50], '')
generator_warning_message_ok_button = Button(screen, [410, 190], [100, 50], SMALL_FONT, 'СТАРТ!')
generator_warning_message_back_button = Button(screen, [290, 190], [100, 50], SMALL_FONT, 'Назад')
generator_warning_message_stop_show_text = Text(screen, EVEN_SMALLER_FONT, [10,180], 'Больше не показывать:')
generator_warning_message_stop_show_switch = Switch(screen, [10,210])

generator_warning_message = Message_window(screen, [520, 250], [generator_warning_message_text1,
                                                              generator_warning_message_text2, 
                                                              generator_warning_message_ok_button,
                                                              generator_warning_message_back_button,
                                                              generator_warning_message_stop_show_text,
                                                              generator_warning_message_stop_show_switch])


settings_title_text = Text(screen, MAIN_FONT, [155,10], 'НАСТРОЙКИ')
settings_video_text = Text(screen, MAIN_FONT, [20,70], 'Заставка')
settings_video_switch = Switch(screen, [430,85], True)
settings_music_text = Text(screen, MAIN_FONT, [20,130], 'Музыка')
settings_music_slider = Slider(screen, [230,150], 250)
settings_sounds_text = Text(screen, MAIN_FONT, [20,190], 'Звуки')
settings_sounds_slider = Slider(screen, [230,210], 250)
settings_fps_text = Text(screen, MAIN_FONT, [20,250], '60 fps')
settings_fps_switch = Switch(screen, [430,265], True)
login_text = Text(screen, MAIN_FONT, [20,310], 'Логин')
login_input = Input_field(screen, [230,310], 250)
clear_login_button = Button(screen, [160,310],[60,60], text='x')
clear_button = Button(screen, [50,400],[400,50], text='Отчистить таблицу')
other_text = Text(screen, SMALL_FONT, [15,460], 'Изменения вступят в силу после перезапуска')
settings_window = Over_Window(screen, SIZE, (500,500), [settings_title_text, 
                                                settings_video_text, 
                                                settings_video_switch, 
                                                settings_music_text,
                                                settings_music_slider,
                                                settings_sounds_text, 
                                                settings_sounds_slider, 
                                                settings_fps_text,
                                                settings_fps_switch,
                                                login_text,
                                                login_input,
                                                clear_login_button,
                                                clear_button,
                                                other_text])


offset = 40
ai_generation_text = Text(screen, MAIN_FONT, [20,10], 'Генерируем...')
ai_generation_model_text = Text(screen, SMALL_FONT, [20, 310], 'Модель: ')
ai_generation_time_text = Text(screen, SMALL_FONT, [20, 70], 'Прошло: ')
ai_generation_answers_text = Text(screen, SMALL_FONT, [20, 100], 'Расписаний пока нет.')
ai_generation_tea_text1 = Text(screen, EVEN_SMALLER_FONT, [20, 170 + offset], 'Пока сходите за чайком,')
ai_generation_tea_text2 = Text(screen, EVEN_SMALLER_FONT, [20, 190 + offset], 'генерация занимает до 5 минут.')
ai_generation_answers_real_text = Text(screen, SMALL_FONT, [20, 130], '')
ai_generation_cancel_button = Button(screen, [355, 290], [125, 40], text='Отмена')
ai_generation_gif = Gif_image(screen, os.path.join(root_path, 'assets', 'loading'), [180, -20])
ai_generation_message = Message_window(screen, [500, 350], [ai_generation_gif,
                                                            ai_generation_text,
                                                            ai_generation_time_text,
                                                            ai_generation_answers_text,
                                                            ai_generation_answers_real_text,
                                                            ai_generation_tea_text1,
                                                            ai_generation_tea_text2,
                                                            ai_generation_model_text,
                                                            ai_generation_cancel_button])

ai_generation_ended_text = Text(screen, MAIN_FONT, [20,10], 'Догенерировал.')
ai_generation_ended_time_text = Text(screen, SMALL_FONT, [20, 70], 'Времени ушло: ')
ai_generation_ended_counter_text = Text(screen, SMALL_FONT, [20, 100], 'Расписаний получилось: ')
ai_generation_ended_back_button = Button(screen, [330, 130], [150, 50], text='Назад')
ai_generation_ended_message = Message_window(screen, [500, 200], [ai_generation_ended_text,
                                                                  ai_generation_ended_time_text,
                                                                  ai_generation_ended_counter_text,
                                                                  ai_generation_ended_back_button])


AI_MORE_MESSAGE_LAST_STATE = 1
ai_more_message_state = 0
def change_ai_more_message_order(direction):
    global ai_more_message_state
    if direction == 'prev':
        if ai_more_message_state == 0:
            ai_more_message_state = AI_MORE_MESSAGE_LAST_STATE
        else:
            ai_more_message_state -= 1
    elif direction == 'next':
        if ai_more_message_state == AI_MORE_MESSAGE_LAST_STATE:
            ai_more_message_state = 0
        else:
            ai_more_message_state += 1


    if ai_more_message_state == 0:
        ai_more_message1.state_closed()
        mond_ai_more_message.state_opened()

    elif ai_more_message_state == 1:
        mond_ai_more_message.state_closed()
        tues_ai_more_message.state_closed()
        wedn_ai_more_message.state_closed()
        thur_ai_more_message.state_closed()
        frid_ai_more_message.state_closed()
        satu_ai_more_message.state_closed()
        ai_more_message1.state_opened()

prev_group_teacher_index = ai_full_subject.selected_index


def update_json_file(file_path, new_undesired_days, new_desired_groups):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        data['undesired_time'] = new_undesired_days
        data['desired_groups'] = new_desired_groups
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            
        return True
    except Exception as e:
        print(e)
        return False
    
def update_config_json():
    try:
        with open(r'config\config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        data['AsmoAI_warning'] = settings['AsmoAI_warning']
        data['TextPrompt_warning'] = settings['TextPrompt_warning']
        data['NoPrompt_warning'] = settings['NoPrompt_warning']
        
        with open(r'config\config.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            
        return True
    except Exception as e:
        print(e)
        return False

def convert_options_to_json():
    desired_groups_dict = {}
    for dict_maker in teacher_group_new_desires:
        if "".join(dict_maker[0]) in desired_groups_dict:
            desired_groups_dict["".join(dict_maker[0])].append(" ".join(dict_maker[1]))
        else:
            desired_groups_dict["".join(dict_maker[0])] = [" ".join(dict_maker[1])]

    undesired_time_dict = dict()
    def add_new_value(key, value):
        if key in undesired_time_dict:
            undesired_time_dict[key].append(value)
        else:
            undesired_time_dict[key] = [value]


    days_mapping = {
    'mond': 'Monday',
    'tues': 'Tuesday',
    'wedn': 'Wednesday',
    'thur': 'Thursday',
    'frid': 'Friday',
    'satu': 'Saturday'
    }

    time_slots = ['8_30', '10_15', '12_00', '14_15', '16_00', '17_40']

    for day_prefix, day_name in days_mapping.items():
        for time_slot in time_slots:
            switch_var = globals().get(f"{day_prefix}_ai_more_message_time_switch_{time_slot}")
            if switch_var and switch_var.state == False:
                add_new_value(day_name, time_slot)

    update_answer = update_json_file(os.path.join(root_path, 'data', 'schedules', 'database', 'Preferences.json'), undesired_time_dict, desired_groups_dict)

    return update_answer




class AI_generation:
    def __init__(self, model_name):
        self.model_name = model_name
        self.waiting_counter = 0
        self.check_delay = 0
        self.check_freq = 120
        self.state = False
        self.files_dir_schedules_ready = os.listdir(os.path.join(root_path, 'src', 'config', 'schedules_ready'))

    def start_generation(self):
        global ai_generation_message, ai_generation_model_text, ai_generation_text, ai_message
        self.promt_users = ai_message_prompt.text
        ai_generation_model_text.text = f'Модель генерации: {self.model_name}'
        ai_message.change_state()
        ai_generation_message.change_state()
        self.start_time = time.time()
        self.state = True
        try:
            for i in self.files_dir_schedules_ready:
                os.remove(os.path.join(root_path, 'src', 'config', 'schedules_ready', i))
        except:
            print('tried to delete previous chat files, but failed(')
        self.files_dir_schedules_ready = os.listdir(os.path.join(root_path, 'src', 'config', 'schedules_ready'))
        self.ready_count_files = len(self.files_dir_schedules_ready)
        self.success_count_files = sum("True" in f for f in self.files_dir_schedules_ready)
        print(self.model_name)
        print(self.promt_users)
        if self.model_name == "AsmoAI":
            os.startfile("asmo_AI.pyw")
        else:
            with open(os.path.join(root_path, "src", "config", f'model_name.txt'), 'w', encoding='utf-8') as f:
                f.write(f"{self.model_name}")
            with open(os.path.join(root_path, "src", "config", f'promt_users.txt'), 'w', encoding='utf-8') as f:
                f.write(f"{self.promt_users}")
            os.startfile("api_sender.pyw") 

    def generation_process(self, mouse_pos, mouse_click, mouse_long_click):
        if self.state:
            global ai_generation_message, ai_generation_text, ai_generation_time_text, ai_generation_answers_text
            self.check_delay += 1
            if self.check_delay == self.check_freq:
                self.files_dir_schedules_ready = os.listdir(os.path.join(root_path, 'src', 'config', 'schedules_ready'))
                self.ready_count_files = len(self.files_dir_schedules_ready)
                self.success_count_files = sum("True" in f for f in self.files_dir_schedules_ready)
                self.check_delay = 0
                if "error.txt" in self.files_dir_schedules_ready:
                    generator_error_message_text2.text = 'Ваши предпочтения некорректны'
                    ai_generation_message.change_state()
                    generator_error_message.change_state()
                    self.state = False
                if self.ready_count_files == 10:
                    for i in self.files_dir_schedules_ready:
                        os.remove(os.path.join(root_path, 'src', 'config', 'schedules_ready', i))
                    ai_generation_ended_time_text.text = f'Времени ушло: {self.cur_time}'
                    ai_generation_ended_counter_text.text = f'Расписаний получилось: {self.success_count_files}'
                    ai_generation_message.change_state()
                    ai_generation_ended_message.change_state()
                    list_ready_variant = os.listdir(os.path.join(root_path, "data", "schedules", "ready"))
                    list_ready_variant = [os.path.join(root_path, "data", "schedules", "ready", variant) for variant in list_ready_variant]
                if 'AsmoAI_Success.txt' in self.files_dir_schedules_ready or 'AsmoAI_Fail.txt' in self.files_dir_schedules_ready:
                    for i in self.files_dir_schedules_ready:
                        os.remove(os.path.join(root_path, 'src', 'config', 'schedules_ready', i))
                    ai_generation_ended_time_text.text = f'Времени ушло: {self.cur_time}'
                    if 'AsmoAI_Success.txt' in self.files_dir_schedules_ready:
                        ai_generation_ended_counter_text.text = 'Расписания были успешно сгенерированы!'
                    elif 'AsmoAI_Fail.txt' in self.files_dir_schedules_ready:
                        ai_generation_ended_counter_text.text = f'При генерации произошла ошибка.'
                    ai_generation_message.change_state()
                    ai_generation_ended_message.change_state()
                    list_ready_variant = os.listdir(os.path.join(root_path, "data", "schedules", "ready"))
                    list_ready_variant = [os.path.join(root_path, "data", "schedules", "ready", variant) for variant in list_ready_variant]
            self.cur_time = round(time.time() - self.start_time, 1)
            ai_generation_time_text.text = f'Прошло {self.cur_time} сек.'
            ai_generation_answers_text.text = f'Получено расписаний: {self.ready_count_files}'
            ai_generation_answers_real_text.text = f'Из них рабочих: {self.success_count_files}'
            ai_generation_message.process(mouse_pos, mouse_click, mouse_long_click)
            ai_generation_ended_message.process(mouse_pos, mouse_click, mouse_long_click)

ai_generation = AI_generation(None)

def reset_all_drop_menus_schedules():
    days = ['mond', 'tues', 'wedn', 'thur', 'frid', 'satu', 'sund']
    times = range(1, 8)  # предполагая, что максимум 7 временных слотов в день
    
    for day in days:
        for time in times:
            var_name = f"{day}{time}"
            if var_name in globals():
                globals()[var_name].selected_index = None

def update_schedule_from_csv(csv_file_path):
    if csv_file_path == None:
        return
    day_prefixes = {
        'Monday': 'mond',
        'Tuesday': 'tues',
        'Wednesday': 'wedn',
        'Thursday': 'thur',
        'Friday': 'frid',
        'Saturday': 'satu',
        'Sunday': 'sund'
    }
    
    time_suffixes = {
        '08:30': '1',
        '10:15': '2',
        '12:00': '3',
        '14:15': '4',
        '16:00': '5',
        '17:40': '6',
    }
    
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            day = row['Day'].strip('"')
            time = row['Time'].strip('"')
            subject = row['Subject'].strip('"').replace('\\', '')
            group = row['Group'].strip('"')
            if time not in ['06:50', '20:50']:
                var_name = f"{day_prefixes[day]}{time_suffixes[time]}"
                globals()[var_name].select_by_main_name_and_group(subject, group)

#SCHEDULE--------------------------------------
list_ready_variant = os.listdir(os.path.join(root_path, "data", "schedules", "ready"))
list_ready_variant = [os.path.join(root_path, "data", "schedules", "ready", variant) for variant in list_ready_variant]
#----------------------------------------------
if len(list_ready_variant) == 0:
    list_ready_variant = [None]
cur_scedule_index = 0

#region MAAAAAAAAAAAX
# Это для завершение api_sender.pyw просто вставь туда где будет кнопка досрочного завершение ОК
#with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', "api_sender.pid")) as f:
#    pid = int(f.read())
#    os.system("taskkill /f /pid " + str(pid))

def f123(Name_subject, Name_group):
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'schedules', 'database', 'schedule.json'), 'r', encoding='utf-8') as f:
        json_temp = json.load(f)
        temp_subject_and_group = []
        for Day, Time, _, _, _ in json_temp[Name_subject][Name_group]:
            temp_subject_and_group.append((Day,Time))
        return temp_subject_and_group
#f123("Физика. Часть 2. Основной уровень", "АТ-16")
#end region


globals_Drop_menu =[]
for day in ['mond','tues','wedn','thur','frid','satu']:
    for time_in_day in range(6,0,-1):
        globals_Drop_menu.append(globals()[f"{day}{time_in_day}"])
running = True
while running:
    if is_mouse_clicked:
        is_long_click = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                is_mouse_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_mouse_clicked = False
                is_long_click = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                for i in globals_Drop_menu:
                    i.scroll_down()

                ai_message_choice_model.scroll_down()
                ai_full_subject.scroll_down()
                ai_full_teacher_group_subject.scroll_down()
                
            elif event.y == -1:
                for i in globals_Drop_menu:
                    i.scroll_up()

                ai_message_choice_model.scroll_up()
                ai_full_subject.scroll_up()
                ai_full_teacher_group_subject.scroll_up()
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pass
            else:
                login_input.new_input(event)
                ai_message_prompt.new_input(event)
        elif event.type == pygame.KEYUP:
            login_input.release_input()
            ai_message_prompt.release_input()

    if CURRENT_THEME == 'DARK':
        screen.fill((30,10,10))
    else:
        screen.fill((100,100,100))

    mouse_pos = pygame.mouse.get_pos()

    table_top_text.process()
    ai_generate_button.process(mouse_pos, is_mouse_clicked, is_long_click)
    scedule_actual_number_text.text = str(cur_scedule_index).zfill(2)
    scedule_actual_number_text.process()

    scedule_number_text.process()
    scedule_actual_number_text.process()
    scedule_back_button.process(mouse_pos, is_mouse_clicked, is_long_click)
    scedule_next_button.process(mouse_pos, is_mouse_clicked, is_long_click)

    for i in globals_Drop_menu:
        i.process(mouse_pos, is_mouse_clicked, is_long_click)

    ai_full_teacher_group_add_text.text = f'Параметров добавлено: {len(teacher_group_new_desires)}'

    if prev_group_teacher_index != ai_full_subject.selected_index:
        ai_full_teacher_group_subject.options = MAIN_SUBJECT_PULL[ai_full_subject.return_system_name_selected()]
        ai_full_teacher_group_subject.selected_index = None

    prev_group_teacher_index = ai_full_subject.selected_index


    if ai_message_prompt_switch.state == 0:
        ai_message_prompt.text = ''

    settings_window.process(mouse_pos, is_mouse_clicked, is_long_click)

    clear_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    ai_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    generator_error_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    generator_warning_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    ai_more_message1.process(mouse_pos, is_mouse_clicked, is_long_click)

    mond_ai_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    tues_ai_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    wedn_ai_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    thur_ai_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    frid_ai_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    satu_ai_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)

    ai_generation.generation_process(mouse_pos, is_mouse_clicked, is_long_click)
    

    if clear_login_button.command():
        login_input.text = ''
    if clear_button.command():
        clear_message.change_state()
    if clear_message_no.command():
        clear_message.change_state()
    if ai_generate_button.command():
        ai_message.change_state()
    if ai_message_cancel_button.command():
        ai_message.change_state()
    if generator_error_message_ok_button.command():
        generator_error_message.change_state()
    if ai_message_start_button.command():
        answer = validate_user_input(ai_message_choice_model.return_system_name_selected(),
                                     ai_message_prompt_switch.state,
                                     ai_message_prompt.text, 
                                     settings)
        if answer[0] == 'error':
            generator_error_message_text2.text = answer[1]
            ai_message.change_state()
            generator_error_message.change_state()
        elif answer[0] == 'warning':
            generator_warning_message_text2.text = answer[1]
            ai_message.change_state()
            generator_warning_message.change_state()
        elif answer[0] == 'pass':
            ai_generation.model_name = ai_message_choice_model.return_list_name_selected()
            ai_generation.start_generation()

    if ai_message_prompt_more_button.command() and ai_message_prompt_switch.state:
        ai_message.change_state()
        mond_ai_more_message.change_state()
    
    if ai_more_message_prev_button1.command():
        change_ai_more_message_order('prev')
    if mond_ai_more_message_next_button.command():
        change_ai_more_message_order('next')
    if ai_more_message_next_button1.command():
        change_ai_more_message_order('next')
    if mond_ai_more_message_prev_button.command():
        change_ai_more_message_order('prev')
    if tues_ai_more_message_next_button.command():
        change_ai_more_message_order('next')
    if wedn_ai_more_message_next_button.command():
        change_ai_more_message_order('next')
    if thur_ai_more_message_next_button.command():
        change_ai_more_message_order('next')
    if frid_ai_more_message_next_button.command():
        change_ai_more_message_order('next')
    if satu_ai_more_message_next_button.command():
        change_ai_more_message_order('next')
    if tues_ai_more_message_prev_button.command():
        change_ai_more_message_order('prev')
    if wedn_ai_more_message_prev_button.command():
        change_ai_more_message_order('prev')
    if thur_ai_more_message_prev_button.command():
        change_ai_more_message_order('prev')
    if frid_ai_more_message_prev_button.command():
        change_ai_more_message_order('prev')
    if satu_ai_more_message_prev_button.command():
        change_ai_more_message_order('prev')
    if ai_full_teacher_group_add_button.command():
        teacher_group_add_new_desire()

    if mond_ai_more_message_next_day_button.command():
        mond_ai_more_message.change_state()
        tues_ai_more_message.change_state()
    if tues_ai_more_message_next_day_button.command():
        tues_ai_more_message.change_state()
        wedn_ai_more_message.change_state()
    if wedn_ai_more_message_next_day_button.command():
        wedn_ai_more_message.change_state()
        thur_ai_more_message.change_state()
    if thur_ai_more_message_next_day_button.command():
        thur_ai_more_message.change_state()
        frid_ai_more_message.change_state()
    if frid_ai_more_message_next_day_button.command():
        frid_ai_more_message.change_state()
        satu_ai_more_message.change_state()
    if satu_ai_more_message_next_day_button.command():
        satu_ai_more_message.change_state()
        mond_ai_more_message.change_state()

    if mond_ai_more_message_prev_day_button.command():
        mond_ai_more_message.change_state()
        satu_ai_more_message.change_state()
    if tues_ai_more_message_prev_day_button.command():
        tues_ai_more_message.change_state()
        mond_ai_more_message.change_state()
    if wedn_ai_more_message_prev_day_button.command():
        wedn_ai_more_message.change_state()
        tues_ai_more_message.change_state()
    if thur_ai_more_message_prev_day_button.command():
        thur_ai_more_message.change_state()
        wedn_ai_more_message.change_state()
    if frid_ai_more_message_prev_day_button.command():
        frid_ai_more_message.change_state()
        thur_ai_more_message.change_state()
    if satu_ai_more_message_prev_day_button.command():
        satu_ai_more_message.change_state()
        frid_ai_more_message.change_state()

    if mond_ai_more_message_back_button.command() or\
            tues_ai_more_message_back_button.command() or \
            wedn_ai_more_message_back_button.command() or \
            thur_ai_more_message_back_button.command() or \
            frid_ai_more_message_back_button.command() or \
            satu_ai_more_message_back_button.command() or \
            ai_more_message_back_button1.command():
        mond_ai_more_message_back_button.already_pressed = False
        tues_ai_more_message_back_button.already_pressed = False
        wedn_ai_more_message_back_button.already_pressed = False
        thur_ai_more_message_back_button.already_pressed = False
        frid_ai_more_message_back_button.already_pressed = False
        satu_ai_more_message_back_button.already_pressed = False
        ai_more_message_back_button1.already_pressed = False
        answer = convert_options_to_json()
        print(answer)

    if mond_ai_more_message_back_button.command():
        mond_ai_more_message.change_state()
        ai_message.change_state()
    if tues_ai_more_message_back_button.command():
        tues_ai_more_message.change_state()
        ai_message.change_state()
    if wedn_ai_more_message_back_button.command():
        wedn_ai_more_message.change_state()
        ai_message.change_state()
    if thur_ai_more_message_back_button.command():
        thur_ai_more_message.change_state()
        ai_message.change_state()
    if frid_ai_more_message_back_button.command():
        frid_ai_more_message.change_state()
        ai_message.change_state()
    if satu_ai_more_message_back_button.command():
        satu_ai_more_message.change_state()
        ai_message.change_state()
    if ai_more_message_back_button1.command():
        ai_more_message1.state_closed()
        ai_message.change_state()

    if ai_generation_ended_back_button.command():
        ai_generation.state = False
        ai_generation_ended_message.change_state()
        list_ready_variant = os.listdir(os.path.join(root_path, "data", "schedules", "ready"))
        list_ready_variant = [os.path.join(root_path, "data", "schedules", "ready", variant) for variant in list_ready_variant]

    if ai_generation_cancel_button.command():
        try:
            time.sleep(0.1)
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', "api_sender.pid")) as f:
                pid = int(f.read())
                os.system("taskkill /f /pid " + str(pid))
            ai_generation.state = False
            ai_generation_message.change_state()
            ai_message.change_state()
        except Exception as e:
            print(f'Error terminating process: {e}')


    if scedule_back_button.command():
        cur_scedule_index -= 1
        if cur_scedule_index == -1:
            cur_scedule_index = len(list_ready_variant) - 1
        reset_all_drop_menus_schedules()
        update_schedule_from_csv(list_ready_variant[cur_scedule_index])
    if scedule_next_button.command():
        cur_scedule_index += 1
        if cur_scedule_index == len(list_ready_variant):
            cur_scedule_index = 0
        reset_all_drop_menus_schedules()
        update_schedule_from_csv(list_ready_variant[cur_scedule_index])

    if mond_ai_more_message_drop_button.command() or\
        tues_ai_more_message_drop_button.command() or\
        wedn_ai_more_message_drop_button.command() or\
        thur_ai_more_message_drop_button.command() or\
        frid_ai_more_message_drop_button.command() or\
        satu_ai_more_message_drop_button.command():
        update_json_file(os.path.join(root_path, 'data', 'schedules', 'database', 'Preferences.json'), {}, {})

    generator_warning_message_back_button_command = generator_warning_message_back_button.command()
    generator_warning_message_ok_button_command = generator_warning_message_ok_button.command()
    if generator_warning_message_back_button_command or generator_warning_message_ok_button_command: 
        if generator_warning_message_stop_show_switch.state:
            if answer[1] == 'Вы собираетесь использовать AsmoAI./Это НЕ ИИ, это АЛГОРИТМ./Он сгенерирует 5 вариантов расписания.':
                settings['AsmoAI_warning'] = True
            elif answer[1] == 'Вы собираетесь использовать текстовый промпт./К сожалению, эта функция очень нестабильна/и часто приводит к сбоям в генерации./Рекомендуем использовать ручные переключатели.':
                settings['TextPrompt_warning'] = True
            elif answer[1] == 'Вы не использовали дополнительных настроек./Это увеличивает шансы на сбой генерации./Рекомендуем выбрать хотя бы пару параметров.':
                settings['NoPrompt_warning'] = True
        print(update_config_json())
        generator_warning_message.change_state()
        ai_message.change_state()
        if generator_warning_message_ok_button_command:
            ai_generation.model_name = ai_message_choice_model.return_list_name_selected()
            ai_generation.start_generation()


    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()