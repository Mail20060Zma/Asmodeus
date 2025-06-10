import pygame
import math

#DARK THEME
HIGHLIGHT_COLOR = (200, 0, 40)
DARKER_HIGHLIGHT_COLOR = (100, 0, 20)
MAIN_COLOR1 = (100, 100, 100)
MAIN_COLOR2 = (80, 80, 80)
MAIN_COLOR3 = (150,150,150)
FONT_COLOR = (200,200,200)
WINDOW_COLOR1 = (50,40,40)
WINDOW_COLOR2 = (40,25,25)


#LIGHT THEME
'''
HIGHLIGHT_COLOR = (255, 130, 0)
DARKER_HIGHLIGHT_COLOR = (255, 180, 150)
MAIN_COLOR1 = (200, 200, 200)
MAIN_COLOR2 = (180, 180, 180)
MAIN_COLOR3 = (250,250,250)
FONT_COLOR = (100,100,100)
WINDOW_COLOR1 = (230,220,220)
WINDOW_COLOR2 = (200,200,200)
'''

CURRENT_THEME = 'DARK'

object_lock = None
over_window_block = None
drop_menu_block = None
used_ids = [000]
drop_menu_ids = [000]

class RainbowColorGenerator:
    def __init__(self, frequency=3, step=0.01):
        self.phase = 0
        self.frequency = frequency
        self.step = step

    def __call__(self):
        r = int(math.sin(self.frequency * self.phase + 0) * 127 + 128)
        g = int(math.sin(self.frequency * self.phase + 2) * 127 + 128)
        b = int(math.sin(self.frequency * self.phase + 4) * 127 + 128)

        self.phase += self.step
        return (r, g, b)

# Создаем генератор
get_rainbow_color = RainbowColorGenerator()

def change_theme():
    global CURRENT_THEME, HIGHLIGHT_COLOR, DARKER_HIGHLIGHT_COLOR, MAIN_COLOR1, MAIN_COLOR2, \
           MAIN_COLOR3, FONT_COLOR, WINDOW_COLOR1, WINDOW_COLOR2
    if CURRENT_THEME == 'DARK':
        CURRENT_THEME = 'LIGHT'
        HIGHLIGHT_COLOR = (255, 130, 0)
        DARKER_HIGHLIGHT_COLOR = (255, 180, 150)
        MAIN_COLOR1 = (200, 200, 200)
        MAIN_COLOR2 = (180, 180, 180)
        MAIN_COLOR3 = (250,250,250)
        FONT_COLOR = (100,100,100)
        WINDOW_COLOR1 = (230,220,220)
        WINDOW_COLOR2 = (200,200,200)
    else:
        CURRENT_THEME = 'DARK'
        HIGHLIGHT_COLOR = (200, 0, 40)
        DARKER_HIGHLIGHT_COLOR = (100, 0, 20)
        MAIN_COLOR1 = (100, 100, 100)
        MAIN_COLOR2 = (80, 80, 80)
        MAIN_COLOR3 = (150,150,150)
        FONT_COLOR = (200,200,200)
        WINDOW_COLOR1 = (50,40,40)
        WINDOW_COLOR2 = (40,25,25)


pygame.init()


MAIN_FONT = pygame.font.Font('CodenameCoderFree4F-Bold.ttf', 44)
BIG_FONT = pygame.font.Font('CodenameCoderFree4F-Bold.ttf', 100)
SMALL_FONT = pygame.font.Font('CodenameCoderFree4F-Bold.ttf', 24)
EVEN_SMALLER_FONT = pygame.font.Font('CodenameCoderFree4F-Bold.ttf', 18)



class Button:
    def __init__(self, screen:pygame.display, pos:list, size:list,
                 font:pygame.font = MAIN_FONT, text:str = ' ', font_custom_pos:list = None,
                 rainbow_highlight = None):
        self.pos = pos
        self.size = size
        self.hover_state = 1 #1-6
        self.click_state = 1 #1-6
        self.screen = screen
        self.font = font
        self.text = text
        self.already_pressed = False
        self.rainbow_highlight = rainbow_highlight

        self.color_state = [[0,0,0] for _ in range(6)]
        if FONT_COLOR[0] > HIGHLIGHT_COLOR[0]:
            cur_index = 0
            for rgb1 in range(FONT_COLOR[0], HIGHLIGHT_COLOR[0], (-1)*(abs(FONT_COLOR[0]-HIGHLIGHT_COLOR[0])//6)):
                self.color_state[cur_index][0] = rgb1
                cur_index += 1
                if cur_index > 5:
                    break
        elif FONT_COLOR[0] == HIGHLIGHT_COLOR[0]:
            for i in range(6):
                self.color_state[i][0] = FONT_COLOR[0]
        else:
            cur_index = 0
            for rgb1 in range(FONT_COLOR[0], HIGHLIGHT_COLOR[0], (abs(FONT_COLOR[0]-HIGHLIGHT_COLOR[0])//6)):
                self.color_state[cur_index][0] = rgb1
                cur_index += 1
                if cur_index > 5:
                    break

        if FONT_COLOR[1] > HIGHLIGHT_COLOR[1]:
            cur_index = 0
            for rgb2 in range(FONT_COLOR[1], HIGHLIGHT_COLOR[1], (-1)*(abs(FONT_COLOR[1]-HIGHLIGHT_COLOR[1])//6)):
                self.color_state[cur_index][1] = rgb2
                cur_index += 1
                if cur_index > 5:
                    break
        elif FONT_COLOR[1] == HIGHLIGHT_COLOR[1]:
            for i in range(6):
                self.color_state[i][1] = FONT_COLOR[1]
        else:
            cur_index = 0
            for rgb2 in range(FONT_COLOR[1], HIGHLIGHT_COLOR[1], (abs(FONT_COLOR[1]-HIGHLIGHT_COLOR[1])//6)):
                self.color_state[cur_index][1] = rgb2
                cur_index += 1
                if cur_index > 5:
                    break

        if FONT_COLOR[2] > HIGHLIGHT_COLOR[2]:
            cur_index = 0
            for rgb3 in range(FONT_COLOR[2], HIGHLIGHT_COLOR[2], (-1)*(abs(FONT_COLOR[2]-HIGHLIGHT_COLOR[2])//6)):
                self.color_state[cur_index][2] = rgb3
                cur_index += 1
                if cur_index > 5:
                    break
        elif FONT_COLOR[2] == HIGHLIGHT_COLOR[2]:
            for i in range(6):
                self.color_state[i][2] = FONT_COLOR[2]
        else:
            cur_index = 0
            for rgb3 in range(FONT_COLOR[2], HIGHLIGHT_COLOR[2], (abs(FONT_COLOR[2]-HIGHLIGHT_COLOR[2])//6)):
                self.color_state[cur_index][2] = rgb3
                cur_index += 1
                if cur_index > 5:
                    break

        self.color_state[0] = FONT_COLOR
        self.color_state[5] = HIGHLIGHT_COLOR


        if not font_custom_pos:
            self.font_pos = [self.size[0]//2-self.font.size(self.text)[0]//2, 
                             self.size[1]//2-self.font.size(self.text)[1]//2-round(self.font.size(self.text)[1]*0.135)]
        else:
            self.font_pos = font_custom_pos
        self.mouse_lock = False

    def _right_to_process(self):
        global over_window_block, drop_menu_block
        if drop_menu_block:
            return False
        if over_window_block:
            try:
                if self.over_window_flag:
                    
                    return True
            except:
                return False
        else:
            return True
    
    def process(self, mouse_pos, click, long_click):
        if self._right_to_process():
            if (self.pos[0] < mouse_pos[0] < self.pos[0]+self.size[0] and \
                self.pos[1] < mouse_pos[1] < self.pos[1]+self.size[1]) or \
                self.mouse_lock:
                if (click and (not long_click)) or (self.mouse_lock):
                    self.hover_state = 6
                    self.click_state = 6
                    self.mouse_lock = True
                
                if not click:
                    self.mouse_lock = False

                self.hover_state += 1
                if self.hover_state > 6:
                    self.hover_state = 6
                self.click_state -= 1
            else:
                self.click_state -= 1
                self.hover_state -= 1
                if self.hover_state < 1:
                    self.hover_state = 1
            
            if self.click_state < 1:
                self.click_state = 1
                self.already_pressed = False
            
        pygame.draw.rect(self.screen, MAIN_COLOR2, [self.pos[0]+5, self.pos[1]+5] + self.size, 0, 20)
        if self.rainbow_highlight:
            pygame.draw.rect(self.screen, get_rainbow_color(), [self.pos[0]+self.click_state, self.pos[1]+self.click_state] + self.size, 0, 20)
        else:
            pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, [self.pos[0]+self.click_state, self.pos[1]+self.click_state] + self.size, 0, 20)
        pygame.draw.rect(self.screen, MAIN_COLOR1, [self.pos[0]+self.hover_state-1+self.click_state, self.pos[1]+self.hover_state-1+self.click_state, 
                                                self.size[0]-(self.hover_state-1)*2, self.size[1]-(self.hover_state-1)*2], 0, 20)
        button_text = self.font.render(self.text, 1, tuple(self.color_state[self.click_state-1]))
        self.screen.blit(button_text, (self.pos[0] + self.font_pos[0] + self.click_state, self.pos[1] + self.font_pos[1] + self.click_state))

    def command(self):
        if self.click_state == 2 and not self.already_pressed:
            self.already_pressed = True
            return True
        return False
    
    def return_essentials(self):
        return ['mouse']
    

class Slider:
    def __init__(self, screen:pygame.display, pos:list, lenght:int, width:int = 20):
        self.screen = screen
        self.pos = pos
        self.lenght = lenght
        self.width = width
        self.state = self.width//2 #self.width//2 - lenght-self.width//2
        self.hover_state = 1 #1-6
        self.mouse_lock = False
        self.one_percent_lenght = (self.lenght-self.width)/100
    
    def _right_to_process(self):
        global over_window_block, drop_menu_block
        if drop_menu_block:
            return False
        if over_window_block:
            try:
                if self.over_window_flag:
                    
                    return True
            except:
                return False
        else:
            return True

    def process(self, mouse_pos, click, long_click):
        if self._right_to_process():
            if self.pos[0] < mouse_pos[0] < self.pos[0]+self.lenght and \
            self.pos[1] < mouse_pos[1] < self.pos[1]+self.width:
                if (click and (not long_click)) or self.mouse_lock:
                    self.state = mouse_pos[0] - self.pos[0]
                    self.hover_state = 6
                    self.mouse_lock = True
                else:
                    self.hover_state += 1
            else:
                self.hover_state -= 1

            if not click:
                self.mouse_lock = False

            if click and self.mouse_lock:
                self.hover_state = 6
                self.state = mouse_pos[0] - self.pos[0]

            if self.hover_state > 6:
                self.hover_state = 6
            elif self.hover_state < 1:
                self.hover_state = 1

            if self.state < self.width//2:
                self.state = self.width//2
            elif self.state > self.lenght-self.width//2:
                self.state = self.lenght-self.width//2

        pygame.draw.rect(self.screen, MAIN_COLOR2, [self.pos[0]+3, self.pos[1]+3] + [self.lenght, self.width], 
                            border_radius = self.width//2)
        pygame.draw.rect(self.screen, MAIN_COLOR1, self.pos + [self.lenght, self.width], border_radius = self.width//2)
        pygame.draw.circle(self.screen, HIGHLIGHT_COLOR, (self.pos[0]+self.state, self.pos[1]+self.width//2), self.width//2+4)
        pygame.draw.circle(self.screen, MAIN_COLOR3, (self.pos[0]+self.state, self.pos[1]+self.width//2), (self.width//2+5)-self.hover_state)
        pygame.draw.circle(self.screen, MAIN_COLOR1, (self.pos[0]+self.state, self.pos[1]+self.width//2), (self.width//2+5)-6)

    def get_value(self):
        #self.width//2 = 0
        #self.lenght-self.width//2 = 100
        return round((self.state-self.width//2) / self.one_percent_lenght)
    
    def return_essentials(self):
        return ['mouse']
            
            
class Text:
    def __init__(self, screen:pygame.display, font:pygame.font.Font, pos:list, text:str):
        self.screen = screen
        self.font = font
        self.pos = pos
        self.text = text

    def process(self):
        text = self.font.render(self.text, 1, FONT_COLOR)
        self.screen.blit(text, self.pos)

    def return_essentials(self):
        return []


class Switch:
    def __init__(self, screen:pygame.display, pos:list, already_on:bool = False):
        self.screen = screen
        self.pos = pos
        self.lenght = 50
        self.width = 30
        if already_on:
            self.state = True
        else: self.state = False
        self.hover_state = 1 #0-5
        self.click_state = 0 #0-20

        self.color_state = [[0,0,0] for _ in range(21)]
        if MAIN_COLOR2[0] > HIGHLIGHT_COLOR[0]:
            cur_index = 0
            for rgb1 in range(MAIN_COLOR2[0], HIGHLIGHT_COLOR[0], (-1)*(abs(MAIN_COLOR2[0]-HIGHLIGHT_COLOR[0])//21)):
                self.color_state[cur_index][0] = rgb1
                cur_index += 1
                if cur_index > 20:
                    break
        elif MAIN_COLOR2[0] == HIGHLIGHT_COLOR[0]:
            for i in range(21):
                self.color_state[i][0] = MAIN_COLOR2[0]
        else:
            cur_index = 0
            for rgb1 in range(MAIN_COLOR2[0], HIGHLIGHT_COLOR[0], (abs(MAIN_COLOR2[0]-HIGHLIGHT_COLOR[0])//21)):
                self.color_state[cur_index][0] = rgb1
                cur_index += 1
                if cur_index > 20:
                    break

        if MAIN_COLOR2[1] > HIGHLIGHT_COLOR[1]:
            cur_index = 0
            for rgb2 in range(MAIN_COLOR2[1], HIGHLIGHT_COLOR[1], (-1)*(abs(MAIN_COLOR2[1]-HIGHLIGHT_COLOR[1])//21)):
                self.color_state[cur_index][1] = rgb2
                cur_index += 1
                if cur_index > 20:
                    break
        elif MAIN_COLOR2[1] == HIGHLIGHT_COLOR[1]:
            for i in range(21):
                self.color_state[i][1] = MAIN_COLOR2[1]
        else:
            cur_index = 0
            for rgb2 in range(MAIN_COLOR2[1], HIGHLIGHT_COLOR[1], (abs(MAIN_COLOR2[1]-HIGHLIGHT_COLOR[1])//21)):
                self.color_state[cur_index][1] = rgb2
                cur_index += 1
                if cur_index > 20:
                    break

        if MAIN_COLOR2[2] > HIGHLIGHT_COLOR[2]:
            cur_index = 0
            for rgb3 in range(MAIN_COLOR2[2], HIGHLIGHT_COLOR[2], (-1)*(abs(MAIN_COLOR2[2]-HIGHLIGHT_COLOR[2])//21)):
                self.color_state[cur_index][2] = rgb3
                cur_index += 1
                if cur_index > 20:
                    break
        elif MAIN_COLOR2[2] == HIGHLIGHT_COLOR[2]:
            for i in range(21):
                self.color_state[i][2] = MAIN_COLOR2[2]
        else:
            cur_index = 0
            for rgb3 in range(MAIN_COLOR2[2], HIGHLIGHT_COLOR[2], (abs(MAIN_COLOR2[2]-HIGHLIGHT_COLOR[2])//21)):
                self.color_state[cur_index][2] = rgb3
                cur_index += 1
                if cur_index > 20:
                    break

        self.color_state[0] = MAIN_COLOR2
        self.color_state[20] = HIGHLIGHT_COLOR

    def _right_to_process(self):
        global over_window_block, drop_menu_block
        if drop_menu_block:
            return False
        if over_window_block:
            try:
                if self.over_window_flag:
                    
                    return True
            except:
                return False
        else:
            return True

    def process(self, mouse_pos, click, long_click):
        if self._right_to_process():
            if self.pos[0] < mouse_pos[0] < self.pos[0]+self.lenght and \
                self.pos[1] < mouse_pos[1] < self.pos[1]+self.width:
                if click and (not long_click):
                    self.hover_state = 5
                    if not self.state:
                        self.state = True
                    else:
                        self.state = False
                
                self.hover_state += 1
                if self.hover_state > 5:
                    self.hover_state = 5
            else:
                self.hover_state -= 1
                if self.hover_state < 0:
                    self.hover_state = 0
            
            if self.state:
                if self.click_state > 3:
                    self.click_state += 5
                else:
                    self.click_state += 1
            else:
                if self.click_state > 17:
                    self.click_state -= 1
                else:
                    self.click_state -= 5
            

            if self.click_state < 0:
                self.click_state = 0
            elif self.click_state > 20:
                self.click_state = 20

        pygame.draw.rect(self.screen, MAIN_COLOR2, [self.pos[0]+2, self.pos[1]+2, self.lenght,self.width], border_radius=self.width//2)
        pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, self.pos+[self.lenght,self.width], border_radius=self.width//2)
        pygame.draw.rect(self.screen, MAIN_COLOR1, [self.pos[0]+self.hover_state, self.pos[1]+self.hover_state,
                            self.lenght - 2*self.hover_state, self.width - 2*self.hover_state], border_radius=self.width//2)
        pygame.draw.circle(self.screen, MAIN_COLOR3, (self.pos[0]+15+self.click_state,self.pos[1]+self.width//2),12)
        pygame.draw.circle(self.screen, tuple(self.color_state[self.click_state]), 
                            (self.pos[0]+15+self.click_state,self.pos[1]+self.width//2),8)
        
    def return_essentials(self):
        return ['mouse']


class Over_Window:
    def __init__(self, screen:pygame.display, screen_size:list, size:tuple, interface:list):
        global used_ids
        self.screen = screen
        self.size = size
        self.interface = interface
        self.showup = False
        self.screen_size = screen_size
        self.start_pos = [self.screen_size[0]//2-self.size[0]//2, 20]
        self.pos = [self.screen_size[0]//2-self.size[0]//2, 20]
        self.back_surf = pygame.Surface((2000,2000), pygame.SRCALPHA)
        for pos_change in self.interface:
            pos_change.local_pos = [pos_change.pos[0], pos_change.pos[1]]
            pos_change.pos[0] += self.screen_size[0]//2-self.size[0]//2
            pos_change.over_window_flag = True
        self.id = used_ids[-1]+1
        used_ids.append(self.id)

    def process(self, mouse_pos, click, long_click):
        global over_window_block
        if over_window_block == self.id:
            self.back_surf.fill((0,0,0,120))
            self.screen.blit(self.back_surf, (0,0))
            self.pos[1] = self.start_pos[1]+5
            pygame.draw.rect(self.screen, WINDOW_COLOR2, [self.pos[0]+5,self.pos[1]+5]+list(self.size), 
                            border_radius = 10)
            pygame.draw.rect(self.screen, WINDOW_COLOR1, [self.pos[0],self.pos[1]]+list(self.size), 
                            border_radius = 10)
            
            if self.showup:
                for processer in self.interface:
                    processer.pos[1] = self.pos[1]+processer.local_pos[1]
                    essentials = processer.return_essentials()
                    if len(essentials) == 0:
                        processer.process()
                    elif len(essentials) == 1:
                        processer.process(mouse_pos, click, long_click)
                    elif len(essentials) == 2:  #INPUT FIELD
                        processer.process(mouse_pos, click, long_click)

    def change_state(self):
        global over_window_block
        if over_window_block == None or over_window_block == self.id:
            if self.showup:
                self.showup = False
                over_window_block = None
            else:
                if not over_window_block:
                    self.showup = True
                    over_window_block = self.id


class Input_field:
    def __init__(self, screen:pygame.display, pos:list, lenght:int, width:int = 60, text:str = '', font:pygame.font = MAIN_FONT):
        self.screen = screen
        self.pos = pos
        self.hover_state = 0 #0-5
        self.marker_state = 0 #0-30
        self.marker_state_up = True
        self.lenght = lenght
        self.width = width
        self.text = text
        self.font = font
        self.font_pos = [self.pos[0] + 10, self.pos[1] + (self.width//2 - self.font.size('a')[1]//2) - 5]
        self.max_text_lenght = (self.lenght - 20) // self.font.size('a')[0] - 1
        self.show_text_index = max(0, len(self.text)-self.max_text_lenght)
        self.lock = False

        self.long_input_start = 0 #0-15
        self.cur_key = None
        self.long_input_marker = 0 #0-1

    def _right_to_process(self):
        global over_window_block, drop_menu_block
        if drop_menu_block:
            return False
        if over_window_block:
            try:
                if self.over_window_flag:
                    return True
            except:
                return False
        else:
            return True

    def process(self, mouse_pos, click, long_click):
        if self._right_to_process():
            if self.pos[0] < mouse_pos[0] < self.pos[0]+self.lenght and \
                self.pos[1] < mouse_pos[1] < self.pos[1]+self.width:
                self.hover_state += 1
                if click and not long_click:
                    self.lock = True
            else:
                self.hover_state -= 1
                if click:
                    self.lock = False
                    self.marker_state = 0
                    self.marker_state_up = True

            if self.lock:
                self.hover_state = 5

                if self.marker_state_up:
                    self.marker_state += 1
                else:
                    self.marker_state -= 1
                if self.marker_state < 0:
                    self.marker_state = 0
                    self.marker_state_up = True
                elif self.marker_state > 30:
                    self.marker_state = 30
                    self.marker_state_up = False

            if self.hover_state < 0:
                self.hover_state = 0
            elif self.hover_state > 5:
                self.hover_state = 5
            
            if self.cur_key != None:
                self.long_input_start += 1
                if self.long_input_start >= 15:
                    self.long_input_start = 15
                    self.long_input_marker += 1
                    if self.long_input_marker == 1:
                        self.long_input_marker = 0
                        if self.cur_key.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += self.cur_key.unicode
                        self.show_text_index = max(0, len(self.text)-self.max_text_lenght)

        self.font_pos = [self.pos[0] + 10, self.pos[1] + (self.width//2 - self.font.size('a')[1]//2) - 5]
        pygame.draw.rect(self.screen, MAIN_COLOR2, [self.pos[0]+3, self.pos[1]+3, self.lenght, self.width],
                                                    border_radius=20)
        pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, self.pos+[self.lenght,self.width], border_radius=20)
        pygame.draw.rect(self.screen, MAIN_COLOR1, [self.pos[0]+self.hover_state, self.pos[1]+self.hover_state,
                                                    self.lenght-self.hover_state*2, self.width-self.hover_state*2],
                                                    border_radius=20)
        marker_surf = pygame.Surface((5, self.width-20))
        marker_surf.set_alpha(self.marker_state*255//20)
        marker_surf.fill(HIGHLIGHT_COLOR)

        self.screen.blit(marker_surf, (self.pos[0]+self.font.size(self.text[self.show_text_index:])[0]+15, 
                                        self.pos[1]+10))
        
        input_text = self.font.render(self.text[self.show_text_index:], 1, FONT_COLOR)
        self.screen.blit(input_text, self.font_pos)


    def new_input(self, new_input):
        if self.lock:
            if new_input.key != pygame.K_BACKSPACE:
                self.text += new_input.unicode
            else:
                self.text = self.text[:-1]
            self.show_text_index = max(0, len(self.text)-self.max_text_lenght)
            self.cur_key = new_input

    def release_input(self):
        self.long_input_start = 0
        self.long_input_marker = 0
        self.cur_key = None
    
    def return_essentials(self):
        return ['mouse', 'keyboard']
    

class Drop_menu_subject:
    def __init__(self, main_name:str, list_name:str, place:str, system_name:str=None, gap_size:int = None,
                 building:str = None, tutor:str = None, group:str = None, lesson_type:str = None):
        self.main_name = main_name
        self.list_name = list_name
        self.place = place
        if system_name:
            self.system_name = system_name
        else:
            self.system_name = self.main_name
        if gap_size:
            self.gap_size = gap_size
            self.main_name = self.main_name.split('/')
        self.building = building
        self.tutor = tutor
        self.group = group
        self.lesson_type = lesson_type
    def give_subject_name(self):
        return self.list_name 
    def give_groupe_name(self):
        return self.group
    def give_teacher_name(self):
        return self.tutor


class Drop_menu:
    def __init__(self, screen:pygame.display, id:str, pos:list, size:list, 
                 options:list, font:pygame.font = SMALL_FONT, options_font:pygame.font = EVEN_SMALLER_FONT, 
                 selected_index=None, visible_options = 5, subject_role = True):
        self.screen = screen
        self.pos = pos
        self.id = id
        self.size = size
        self.options = options
        self.selected_index = selected_index
        self.hover_state = 0 #0-5
        self.is_opened = False
        self.font = font
        self.options_font = options_font
        self.drop_menu_height = self.options_font.size('a')[1]+10
        self.drop_menu_index = 0
        self.visible_options = visible_options
        global drop_menu_ids
        self.drop_menu_id = drop_menu_ids[-1]+1
        drop_menu_ids.append(self.drop_menu_id)

        if subject_role:
            pass

    def _right_to_process(self):
        global over_window_block, drop_menu_block
        if over_window_block:
            if not drop_menu_block:
                try:
                    if self.over_window_flag:
                        return True
                except:
                    return False
            else:
                if drop_menu_block == self.drop_menu_id:
                    return True
                else:
                    return False
        else:
            if drop_menu_block:
                if drop_menu_block == self.drop_menu_id:
                    return True
                else:
                    return False
            return True

    def process(self, mouse_pos, is_mouse_clicked, is_long_click):
        global object_lock

        if self._right_to_process():
            
            if self.is_opened:
                self.hover_state = 5

            if self.is_opened:
                options_counter = 0
                if len(self.options) != 0:
                    while (options_counter <= self.visible_options-1) and (options_counter != len(self.options)):
                        option_tile_rect = [self.pos[0], 
                                            self.pos[1]+self.size[1]+options_counter*self.drop_menu_height, 
                                            self.size[0],
                                            self.drop_menu_height]
                        if option_tile_rect[0] < mouse_pos[0] < option_tile_rect[0]+option_tile_rect[2] and\
                            option_tile_rect[1] < mouse_pos[1] < option_tile_rect[1]+option_tile_rect[3]:
                            pygame.draw.rect(self.screen, DARKER_HIGHLIGHT_COLOR, option_tile_rect)
                            if is_mouse_clicked and not is_long_click:
                                self.selected_index = options_counter + self.drop_menu_index
                        else:
                            pygame.draw.rect(self.screen, MAIN_COLOR2, option_tile_rect)
                    
                        changed_option_text = self.options[options_counter+self.drop_menu_index].list_name
                        if options_counter+self.drop_menu_index == self.selected_index:
                            option_text = self.options_font.render(changed_option_text,
                                                                    1, HIGHLIGHT_COLOR)
                        else:
                            option_text = self.options_font.render(changed_option_text,
                                                                    1, FONT_COLOR)
                        options_text_x = self.size[0]//2+self.pos[0]-self.options_font.size(changed_option_text)[0]//2
                        options_text_y = self.size[1]+self.pos[1]+self.drop_menu_height//2+options_counter*self.drop_menu_height\
                                        -self.options_font.size(changed_option_text)[1]//2
                        
                        self.screen.blit(option_text, [options_text_x, options_text_y])
                        
                        options_counter += 1
                    
                    if options_counter + self.drop_menu_index != len(self.options):
                        polygon_start_pos = (self.pos[0]+self.size[0]-10, 
                                            self.pos[1]+self.size[1]+self.drop_menu_height*self.visible_options-10)
                        pygame.draw.polygon(self.screen, FONT_COLOR, [polygon_start_pos, 
                                                                    (polygon_start_pos[0]+6, polygon_start_pos[1]),
                                                                    (polygon_start_pos[0]+3, polygon_start_pos[1]+6)])
                        
                    if self.drop_menu_index != 0:
                        polygon_start_pos = (self.pos[0]+self.size[0]-10, 
                                            self.pos[1]+self.size[1]+6)
                        pygame.draw.polygon(self.screen, FONT_COLOR, [(polygon_start_pos[0], polygon_start_pos[1]+6), 
                                                                    (polygon_start_pos[0]+6, polygon_start_pos[1]+6),
                                                                    (polygon_start_pos[0]+3, polygon_start_pos[1])])
        
            global drop_menu_block
            if self.is_opened:
                drop_menu_block = self.drop_menu_id
            else:
                drop_menu_block = None
                    
            if self.pos[0] <= mouse_pos[0] <= self.pos[0]+self.size[0] and\
                self.pos[1] <= mouse_pos[1] <= self.pos[1]+self.size[1]:
                if not object_lock:
                    self.hover_state += 1
                if is_mouse_clicked and not is_long_click and not object_lock:
                    self.is_opened = True
                    object_lock = self.id
            else:
                if is_mouse_clicked:
                    self.is_opened = False
                    self.drop_menu_index = 0
                    if object_lock == self.id:
                        object_lock = None
                if not self.is_opened:
                    self.hover_state -= 1

            if self.hover_state > 5:
                self.hover_state = 5
            elif self.hover_state < 0:
                self.hover_state = 0

        pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, self.pos+self.size)
        pygame.draw.rect(self.screen, MAIN_COLOR1, [self.pos[0]+self.hover_state, self.pos[1]+self.hover_state,
                                                    self.size[0]-2*self.hover_state, self.size[1]-2*self.hover_state])
        
        if self.selected_index != None:
            show_text = self.options[self.selected_index].main_name
            if len(show_text) > 1:
                show_text_height = len(show_text)*self.font.size('a')[1]//2+\
                                    (self.options[self.selected_index].gap_size)*(len(show_text)-1)
            else:
                show_text_height = self.font.size('a')[1]
            
            show_text_lenght = 0
            for text_max_lenght in show_text:
                show_text_lenght = max(show_text_lenght, self.font.size(text_max_lenght)[0])

            text_x = self.size[0]//2-show_text_lenght//2+self.pos[0]
            text_y = self.size[1]//2-show_text_height//2+self.pos[1]

            for main_text_print in show_text:
                rendered_row = self.font.render(main_text_print, 1, FONT_COLOR)
                self.screen.blit(rendered_row, [text_x, text_y])
                text_y += self.options[self.selected_index].gap_size

            place_text = self.options_font.render(self.options[self.selected_index].place, 1, FONT_COLOR)
            self.screen.blit(place_text, (self.pos[0]+self.size[0]-50, self.pos[1]+8))

    def scroll_up(self):
        if self._right_to_process():
            if self.is_opened and (self.drop_menu_index+1) < (len(self.options)-self.visible_options+1):
                self.drop_menu_index += 1

    def scroll_down(self):
        if self._right_to_process():
            if self.is_opened and (self.drop_menu_index-1) >= 0:
                self.drop_menu_index -= 1

    def return_essentials(self):
        return ['mouse']
    
    def return_selected(self):
        if self.selected_index != None:
            return self.options[self.selected_index].system_name
        return None
    
    def return_main_name_selected(self):
        if self.selected_index != None:
            return self.options[self.selected_index].main_name
        return None


class Message_window:
    def __init__(self, screen:pygame.display, size:list, interface:list):
        global used_ids
        self.screen = screen
        self.size = size
        screen_x, screen_y = self.screen.get_size()
        center = [screen_x//2, screen_y//2]
        self.pos = [center[0]-self.size[0]//2, center[1]-self.size[1]//2]
        self.interface = interface
        for pos_change in self.interface:
            pos_change.pos[0] += self.pos[0]
            pos_change.pos[1] += self.pos[1]
            pos_change.over_window_flag = True
        self.id = used_ids[-1]+1
        used_ids.append(self.id)
        self.state = 0
        self.prev_id = 0

    def process(self, mouse_pos, click, long_click):
        if self.state:
            self.back_surf = pygame.Surface((2000,2000), pygame.SRCALPHA)
            self.back_surf.fill((0,0,0,120))
            self.screen.blit(self.back_surf, (0,0))
            pygame.draw.rect(self.screen, WINDOW_COLOR2, [self.pos[0] + 5, self.pos[1] + 5] + self.size, 
                            border_radius = 10)
            pygame.draw.rect(self.screen, WINDOW_COLOR1, self.pos + self.size, 
                            border_radius = 10)

            for processer in self.interface:
                essentials = processer.return_essentials()
                if len(essentials) == 0:
                    processer.process()
                elif len(essentials) == 1:
                    processer.process(mouse_pos, click, long_click)
                elif len(essentials) == 2:  #INPUT FIELD
                    processer.process(mouse_pos, click, long_click)

    def change_state(self):
        global over_window_block
        if self.state:
            self.state = 0
            over_window_block = self.prev_id
        else:
            self.prev_id = over_window_block
            self.state = 1
            over_window_block = self.id

    def state_closed(self):
        global over_window_block
        if self.state:
            self.state = 0
            over_window_block = self.prev_id

    def state_opened(self):
        global over_window_block
        if not self.state:
            self.prev_id = over_window_block
            self.state = 1
            over_window_block = self.id