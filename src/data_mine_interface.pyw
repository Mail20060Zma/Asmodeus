import pygame
import sys
import asmo_UI
import os
import data_mine_final

pygame.init()

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = 1280, 720  # 720p разрешение (1280x720)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AsmoMiner v0.8.0")
BACKGROUND = (0, 0, 0)

programIcon = pygame.image.load(os.path.join(root_path, 'assets', 'icon1.png'))
pygame.display.set_icon(programIcon)

current_slide = 0
slides = []
for i in range(1, 12):
    try:
        slide = pygame.image.load(os.path.join(root_path, 'assets', 'download_agent', f'slide{i}.png'))
        slide = pygame.transform.scale(slide, (WIDTH, HEIGHT))
        slides.append(slide)
    except:
        print(f"Ошибка загрузки slide{i}.png")
        blank_slide = pygame.Surface((WIDTH, HEIGHT))
        blank_slide.fill(BACKGROUND)
        font = pygame.font.SysFont(None, 48)
        text = font.render(f"slide{i}.png не найден", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        blank_slide.blit(text, text_rect)
        slides.append(blank_slide)

button_backward = asmo_UI.Button(screen, [20, 650], [50, 50], text='<')
slide_text = asmo_UI.Text(screen, asmo_UI.SMALL_FONT, [90, 660], f"Слайд {current_slide + 1}/{len(slides)-2}")
button_forward = asmo_UI.Button(screen, [205, 650], [50, 50], text='>')

start_button = asmo_UI.Button(screen, [800, 600], [460, 100], text='Начать обработку')
folder_button = asmo_UI.Button(screen, [800, 600], [460, 100], text='Открыть папку')

if not slides:
    print("Не найдено ни одного слайда!")
    pygame.quit()
    sys.exit()

def change_slide(direction):
    """Функция для переключения слайдов"""
    global current_slide
    current_slide += direction
    
    if current_slide < 0:
        current_slide = 8
    elif current_slide > 8:
        current_slide = 0
        
    return current_slide

clock = pygame.time.Clock()
running = True

is_mouse_clicked = False
is_long_click = False
program_ended = False

while running:
    if is_mouse_clicked:
        is_long_click = True
    
    mouse_pos = pygame.mouse.get_pos()

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change_slide(-1)  
            elif event.key == pygame.K_RIGHT:
                change_slide(1)   
            elif event.key == pygame.K_ESCAPE:
                running = False   
    
    if button_backward.command():
        change_slide(-1)
    elif button_forward.command():
        change_slide(1)
    
    if folder_button.command():
        os.startfile(os.path.join(root_path, 'data', 'schedules', 'isc'))

    if start_button.command():
        answer = data_mine_final.main_data_mine_final()
        if answer == True:
            current_slide = 9
        else:
            current_slide = 10
        current_slide = 9
    
    screen.fill(BACKGROUND)
    screen.blit(slides[current_slide], (0, 0))

    if 0 <= current_slide <= 8:
        button_backward.process(mouse_pos, is_mouse_clicked, is_long_click)
        slide_text.process()
        button_forward.process(mouse_pos, is_mouse_clicked, is_long_click)
        slide_text.text = f"Слайд {current_slide + 1}/{len(slides)-2}"
        if current_slide == 8:
            start_button.process(mouse_pos, is_mouse_clicked, is_long_click)
        if current_slide == 7:
            folder_button.process(mouse_pos, is_mouse_clicked, is_long_click)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()