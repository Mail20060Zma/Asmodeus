import pygame
import os
from asmo_UI import *

START_MOVIE = True

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
size = [1280, 720]
screen = pygame.display.set_mode(size, pygame.NOFRAME)
clock = pygame.time.Clock()
MAIN_FONT = pygame.font.Font(os.path.join(root_path, 'assets', 'CodenameCoderFree4F-Bold.ttf'), 44)

running = True
LAST_FRAME = 121
if START_MOVIE:
    cur_frame = 1
else: cur_frame = LAST_FRAME

is_mouse_clicked = False
is_long_click = False

pygame.mixer.music.load(os.path.join(root_path, 'assets', 'startup', 'start_sound.mp3'))
pygame.mixer.music.play()

interface_button = Button(screen, [800,550], [400,100], text='Обработка данных')
collect_button = Button(screen, [350,550], [400,100], text='Сбор данных')
exit_button = Button(screen, [80,550], [220,100], text='Выход')

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

    mouse_pos = pygame.mouse.get_pos()

    video_surf = pygame.image.load(os.path.join(root_path, 'assets', 'startup', f'0001.png{'0'*(4-len(str(cur_frame)))}{cur_frame}.png'))
    video_rect = video_surf.get_rect(bottomright=size)
    screen.blit(video_surf, video_rect)

    if cur_frame != LAST_FRAME:
        cur_frame += 1
    else:
        interface_button.process(mouse_pos, is_mouse_clicked, is_long_click)
        collect_button.process(mouse_pos, is_mouse_clicked, is_long_click)
        exit_button.process(mouse_pos, is_mouse_clicked, is_long_click)

    
    if exit_button.command():
        running = False
    elif interface_button.command():
        running = False
        os.startfile('interface.pyw')
    elif collect_button.command():
        running = False
        os.startfile('data_mine_interface.pyw')

    


    pygame.display.flip()
    clock.tick(30)
pygame.quit()

