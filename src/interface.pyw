import pygame
import sys
from collections import defaultdict
from asmo_UI import *
from ai_generate_validator import *
from schedule_converter_interface import *

FPS = 60

pygame.init()


SIZE = [1350, 800]
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Asmodeus build 10.06.25')
clock = pygame.time.Clock()
programIcon = pygame.image.load(r'assets\icon2.png')
pygame.display.set_icon(programIcon)

def play_sound(file_path):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_path)
    sound.play()


is_mouse_clicked = False
is_long_click = False

debug_subject_pull = [Drop_menu_subject('Физика и/основы механики', 'Физика', 'ГУК-4', 'physics', 20),
                    Drop_menu_subject('Дополнительные/главы математики', 'ДГМ', 'Р-445', 'dgm', 20),
                    Drop_menu_subject('Программирование/(прод. уровень)', 'Прога (прод)', 'Р-145', 'progA', 20),
                    Drop_menu_subject('Векторный/анализ','Вект.ан.','Р-205','VecAlg',20)]

MAIN_SUBJECT_PULL = csv_to_schedule_dict('schedule.csv')

ai_pull = [Drop_menu_subject('DeepSeek R1', 'Deepseek', '', gap_size=20),
           Drop_menu_subject('AsmoAI(no text)', 'AsmoAI', '', gap_size=20),
           Drop_menu_subject('Llama', 'Llama', '', gap_size=20),
           Drop_menu_subject('Qwen3-235B-A22B', 'Qwen3', '', gap_size=20),
           Drop_menu_subject('Qwen2.5-72B', 'Qwen2.5', '', gap_size=20)]

teacher_group_new_desires = []

def teacher_group_add_new_desire():
    global teacher_group_new_desires
    new_desire = [ai_full_subject.return_main_name_selected(), ai_full_teacher_group_subject.return_main_name_selected()]
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

ai_generate_button = Button(screen, [50, 720], [400, 60], text = 'Сгенерировать с ИИ')

ai_message_text_model = Text(screen, SMALL_FONT, [10,20], 'Агент генерации: ')
ai_message_choice_model = Drop_menu(screen, 'ai_choice', [210, 10], [190, 50], ai_pull)
ai_message_prompt_switch_text = Text(screen, SMALL_FONT, [10, 75], 'Доп.Промпт: ')
ai_message_prompt_switch = Switch(screen, [150, 75], already_on=True)
ai_message_prompt_more_button = Button(screen, [220, 75], [160, 30], SMALL_FONT, 'Больше опций')
ai_message_prompt_text = Text(screen, SMALL_FONT, [10, 130], 'Промпт: ')
ai_message_prompt = Input_field(screen, [100, 130], 300, 40, font=SMALL_FONT)
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
                mond1.scroll_down()
                mond2.scroll_down()
                mond3.scroll_down()
                mond4.scroll_down()
                mond5.scroll_down()
                mond6.scroll_down()

                tues1.scroll_down()
                tues2.scroll_down()
                tues3.scroll_down()
                tues4.scroll_down()
                tues5.scroll_down()
                tues6.scroll_down()

                wedn1.scroll_down()
                wedn2.scroll_down()
                wedn3.scroll_down()
                wedn4.scroll_down()
                wedn5.scroll_down()
                wedn6.scroll_down()

                thur1.scroll_down()
                thur2.scroll_down()
                thur3.scroll_down()
                thur4.scroll_down()
                thur5.scroll_down()
                thur6.scroll_down()

                frid1.scroll_down()
                frid2.scroll_down()
                frid3.scroll_down()
                frid4.scroll_down()
                frid5.scroll_down()
                frid6.scroll_down()

                satu1.scroll_down()
                satu2.scroll_down()
                satu3.scroll_down()
                satu4.scroll_down()
                satu5.scroll_down()
                satu6.scroll_down()

                ai_message_choice_model.scroll_down()
                ai_full_subject.scroll_down()
                ai_full_teacher_group_subject.scroll_down()
                
            elif event.y == -1:
                mond1.scroll_up()
                mond2.scroll_up()
                mond3.scroll_up()
                mond4.scroll_up()
                mond5.scroll_up()
                mond6.scroll_up()

                tues1.scroll_up()
                tues2.scroll_up()
                tues3.scroll_up()
                tues4.scroll_up()
                tues5.scroll_up()
                tues6.scroll_up()

                wedn1.scroll_up()
                wedn2.scroll_up()
                wedn3.scroll_up()
                wedn4.scroll_up()
                wedn5.scroll_up()
                wedn6.scroll_up()

                thur1.scroll_up()
                thur2.scroll_up()
                thur3.scroll_up()
                thur4.scroll_up()
                thur5.scroll_up()
                thur6.scroll_up()

                frid1.scroll_up()
                frid2.scroll_up()
                frid3.scroll_up()
                frid4.scroll_up()
                frid5.scroll_up()
                frid6.scroll_up()

                satu1.scroll_up()
                satu2.scroll_up()
                satu3.scroll_up()
                satu4.scroll_up()
                satu5.scroll_up()
                satu6.scroll_up()

                ai_message_choice_model.scroll_up()
                ai_full_subject.scroll_up()
                ai_full_teacher_group_subject.scroll_up()
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                settings_window.change_state()
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

    mond6.process(mouse_pos, is_mouse_clicked, is_long_click)
    mond5.process(mouse_pos, is_mouse_clicked, is_long_click)
    mond4.process(mouse_pos, is_mouse_clicked, is_long_click)
    mond3.process(mouse_pos, is_mouse_clicked, is_long_click)
    mond2.process(mouse_pos, is_mouse_clicked, is_long_click)
    mond1.process(mouse_pos, is_mouse_clicked, is_long_click)

    tues6.process(mouse_pos, is_mouse_clicked, is_long_click)
    tues5.process(mouse_pos, is_mouse_clicked, is_long_click)
    tues4.process(mouse_pos, is_mouse_clicked, is_long_click)
    tues3.process(mouse_pos, is_mouse_clicked, is_long_click)
    tues2.process(mouse_pos, is_mouse_clicked, is_long_click)
    tues1.process(mouse_pos, is_mouse_clicked, is_long_click)

    wedn6.process(mouse_pos, is_mouse_clicked, is_long_click)
    wedn5.process(mouse_pos, is_mouse_clicked, is_long_click)
    wedn4.process(mouse_pos, is_mouse_clicked, is_long_click)
    wedn3.process(mouse_pos, is_mouse_clicked, is_long_click)
    wedn2.process(mouse_pos, is_mouse_clicked, is_long_click)
    wedn1.process(mouse_pos, is_mouse_clicked, is_long_click)

    thur6.process(mouse_pos, is_mouse_clicked, is_long_click)
    thur5.process(mouse_pos, is_mouse_clicked, is_long_click)
    thur4.process(mouse_pos, is_mouse_clicked, is_long_click)
    thur3.process(mouse_pos, is_mouse_clicked, is_long_click)
    thur2.process(mouse_pos, is_mouse_clicked, is_long_click)
    thur1.process(mouse_pos, is_mouse_clicked, is_long_click)

    frid6.process(mouse_pos, is_mouse_clicked, is_long_click)
    frid5.process(mouse_pos, is_mouse_clicked, is_long_click)
    frid4.process(mouse_pos, is_mouse_clicked, is_long_click)
    frid3.process(mouse_pos, is_mouse_clicked, is_long_click)
    frid2.process(mouse_pos, is_mouse_clicked, is_long_click)
    frid1.process(mouse_pos, is_mouse_clicked, is_long_click)

    satu6.process(mouse_pos, is_mouse_clicked, is_long_click)
    satu5.process(mouse_pos, is_mouse_clicked, is_long_click)
    satu4.process(mouse_pos, is_mouse_clicked, is_long_click)
    satu3.process(mouse_pos, is_mouse_clicked, is_long_click)
    satu2.process(mouse_pos, is_mouse_clicked, is_long_click)
    satu1.process(mouse_pos, is_mouse_clicked, is_long_click)


    ai_full_teacher_group_add_text.text = f'Параметров добавлено: {len(teacher_group_new_desires)}'

    if prev_group_teacher_index != ai_full_subject.selected_index:
        ai_full_teacher_group_subject.options = MAIN_SUBJECT_PULL[ai_full_subject.return_selected()]
        ai_full_teacher_group_subject.selected_index = None

    prev_group_teacher_index = ai_full_subject.selected_index


    if ai_message_prompt_switch.state == 0:
        ai_message_prompt.text = ''

    settings_window.process(mouse_pos, is_mouse_clicked, is_long_click)

    clear_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    ai_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    generator_error_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    ai_more_message1.process(mouse_pos, is_mouse_clicked, is_long_click)

    mond_ai_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    tues_ai_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    wedn_ai_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    thur_ai_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    frid_ai_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    satu_ai_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    

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
        answer = validate_user_input(ai_message_choice_model.return_selected(),
                                     ai_message_prompt_switch.state,
                                     ai_message_prompt.text)
        if answer[0] == 'error':
            generator_error_message_text2.text = answer[1]
            ai_message.change_state()
            generator_error_message.change_state()
    if ai_message_prompt_more_button.command() and ai_message_prompt_switch.state:
        ai_message.change_state()
        mond_ai_more_message.change_state()
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


    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()