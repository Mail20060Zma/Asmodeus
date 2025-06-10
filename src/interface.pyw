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
pygame.display.set_caption('Asmodeus build 30.05.25')
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

ai_more_message_day_text = Text(screen, SMALL_FONT, [10,5], 'Дни учёбы:')
ai_more_message_day_text1 = Text(screen, SMALL_FONT, [10,40], 'Понедельник          Четверг')
ai_more_message_day_text2 = Text(screen, SMALL_FONT, [10,80], 'Вторник              Пятница')
ai_more_message_day_text3 = Text(screen, SMALL_FONT, [10,120], 'Среда                Суббота')
ai_more_message_day_switch_mond = Switch(screen, [150, 40], True)
ai_more_message_day_switch_thu = Switch(screen, [330, 40], True)
ai_more_message_day_switch_tue = Switch(screen, [150, 80], True)
ai_more_message_day_switch_fri = Switch(screen, [330, 80], True)
ai_more_message_day_switch_wed = Switch(screen, [150, 120], True)
ai_more_message_day_switch_sat = Switch(screen, [330, 120], True)
ai_more_message_back_button = Button(screen, [280, 160], [100,30], SMALL_FONT, 'Назад')
ai_message_fucking_more_button = Button(screen, [10, 160], [260, 30], SMALL_FONT, 'МНЕ НУЖНО БОЛЬШЕ ОПЦИЙ')
ai_more_message = Message_window(screen, [395,205], [ai_more_message_day_text,
                                                     ai_more_message_day_text1,
                                                     ai_more_message_day_text2,
                                                     ai_more_message_day_text3,
                                                     ai_more_message_day_switch_sat,
                                                     ai_more_message_day_switch_fri,
                                                     ai_more_message_day_switch_thu,
                                                     ai_more_message_day_switch_wed,
                                                     ai_more_message_day_switch_tue,
                                                     ai_more_message_day_switch_mond,
                                                     ai_more_message_back_button,
                                                     ai_message_fucking_more_button])

ai_more_more_message_title = Text(screen, SMALL_FONT, [10, 5], 'Выбор предметов, групп и преподавателей:')
ai_full_subject = Drop_menu(screen, 'ai_all_subject', [30,40], [200,100], MAIN_SUBJECT_PULL['All_subject'])
ai_full_teacher_groupe_subject = Drop_menu(screen, 'ai_all_info_subject', [270,40], [200,100], MAIN_SUBJECT_PULL['Дополнительные главы математики. ИРИТ-РТФ (09 УГН)'])
ai_more_more_message_back_button = Button(screen, [385, 160], [100,30], SMALL_FONT, 'Назад')
ai_more_more_message = Message_window(screen, [500,205], [ai_more_more_message_title,
                                                          ai_more_more_message_back_button,
                                                          ai_full_subject,
                                                          ai_full_teacher_groupe_subject])

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
                ai_full_teacher_groupe_subject.scroll_down()
                
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
                ai_full_teacher_groupe_subject.scroll_up()
                
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

    if  Drop_menu.return_main_name_selected(ai_full_subject):
        ai_full_teacher_groupe_subject = Drop_menu(screen, 'satu61', [270,40], [200,100], MAIN_SUBJECT_PULL[Drop_menu.return_selected(ai_full_subject)])


    if ai_message_prompt_switch.state == 0:
        ai_message_prompt.text = ''

    settings_window.process(mouse_pos, is_mouse_clicked, is_long_click)

    clear_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    ai_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    ai_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    generator_error_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    ai_more_more_message.process(mouse_pos, is_mouse_clicked, is_long_click)
    

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
        ai_more_message.change_state()
    if ai_more_message_back_button.command():
        ai_more_message.change_state()
        ai_message.change_state()
    if ai_more_more_message_back_button.command():
        ai_more_more_message.change_state()
        ai_more_message.change_state()
    if ai_message_fucking_more_button.command():
        #play_sound('assets/aaaaa_sound.mp3')
        ai_more_message.change_state()
        ai_more_more_message.change_state()

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()