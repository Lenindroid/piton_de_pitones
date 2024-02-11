import pygame
import random
from pygame.math import Vector2

# pygame setup
pygame.init()
cell_size = 40
cell_number_x = 20
cell_number_y = 15
screen = pygame.display.set_mode((cell_size * cell_number_x, cell_size * cell_number_y))
pygame.display.set_caption('Pitón de pitones (Alpha 1.0.9)')
clock = pygame.time.Clock()
running = True
game_state = 'MENU'
score = 0

# defining classes
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.head_down = pygame.image.load('assets\snake\head.png').convert_alpha()
        self.head_images = {
        'down': self.head_down,
        'left': pygame.transform.rotozoom(self.head_down, 270, 1),
        'right': pygame.transform.rotozoom(self.head_down, 90, 1),
        'up': pygame.transform.rotozoom(self.head_down, 180, 1)
        }

        self.pythons_assets = [self.head_images['down']]
        self.maybepythons = [{'image': 'assets\snake\head.png', 'position': Vector2(3, 3)}, {'image': 'assets\snake\head.png', 'position': Vector2(2, 3)}]
        self.rect = self.head_down.get_rect(topleft=(40, 300))
        self.is_moving = 'right'
        
    def spawn(self):
        for python in self.maybepythons:
            image = pygame.image.load(python['image']).convert_alpha()
            x_position = int(cell_size * python['position'].y)
            y_position = int(cell_size * python['position'].x)
            rect = image.get_rect(topleft=(x_position, y_position))
            screen.blit(image, rect)
    
    def move_left(self):
        self.rect.x -= 10
    
    def new_move_left(self):
        previous_position = None
        next_position = None
        for i, python in enumerate(self.maybepythons):
            if i == 0:
                next_position = python['position']
                previous_position = python['position']
                python['position'].x -= 1
            else: 
                next_position =  python['position']
                python['position'] = previous_position
    
    def move_right(self):
        self.rect.x += 10
    
    def new_move_right(self):
        previous_position = None
        next_position = None
        for i, python in enumerate(self.maybepythons):
            if i == 0:
                next_position = python['position']
                previous_position = python['position']
                python['position'].x += 1
            else: 
                next_position =  python['position']
                python['position'] = previous_position
    
    def move_up(self):
        self.rect.y -= 10
    
    def new_move_up(self):
        previous_position = None
        next_position = None
        for i, python in enumerate(self.maybepythons):
            if i == 0:
                next_position = python['position']
                previous_position = python['position']
                python['position'].y -= 1
            else: 
                next_position =  python['position']
                python['position'] = previous_position
    
    def move_down(self):
        self.rect.y += 10
        
    def new_move_down(self):
        previous_position = None
        next_position = None
        for i, python in enumerate(self.maybepythons):
            if i == 0:
                next_position = python['position']
                previous_position = python['position']
                python['position'].y += 1
            else: 
                next_position =  python['position']
                python['position'] = previous_position

class Python:
    def __init__(self):
        self.x = random.randint(0, cell_number_x - 1)
        self.y = random.randint(0, cell_number_y - 1)
        self.position = Vector2(cell_size * self.x, self.y * 5)
        self.rect = pygame.rect.Rect(self.position.x, self.position.y, cell_size, cell_size)
        self.should_spawn = True
        self.pythons_assets = ['assets\snake\cat_python.png', 'assets\snake\legacy_lenin.png', 'assets\snake\gabriela_python.png']
        
    def spawn(self):
        image = pygame.image.load(self.pythons_assets[0]).convert()
        screen.blit(image, self.position)
    
    def switch_spawn(self):
        random.shuffle(self.pythons_assets)
        self.x = random.randint(0, cell_number_x - 1)
        self.y = random.randint(0, cell_number_y - 1)
        self.position = Vector2(cell_size * self.x, self.y * 5)
        self.rect = pygame.rect.Rect(self.position.x, self.position.y, cell_size, cell_size)

class Static_Image (pygame.sprite.Sprite):
    def __init__(self, route, alpha, **rectangle):
        super().__init__()
        if (alpha): 
            self.image = pygame.image.load(route).convert_alpha()
        else: 
            self.image = pygame.image.load(route).convert()
            
        self.rect = self.image.get_rect(**rectangle)
        
class Font(pygame.sprite.Sprite):
    def __init__(self, font, size):
        super().__init__()
        self.font_config = pygame.font.Font(font, size)

        
    def render (self, text, AA, color):
        text_sufrace = self.font_config.render(text, AA, color)
        return text_sufrace
    
class Music(pygame.sprite.Sprite):
    def __init__(self, file):
        super().__init__()
        self.file = pygame.mixer.Sound(file)

# loading assets
grass = Static_Image('assets\grass.png', False, topleft = (0, 0))
logo = Static_Image('assets\logo.png', True, center = (400, 150))
button_play = Static_Image('assets\play_button.png', True, topleft = (200, 186))
button_play_again = Static_Image('assets\play_again.png', True, topleft = (52, 488))
snake = Snake()
python = Python()
death_message = Static_Image('assets\DEATH_MESSAGE.png', True, topleft = (0, 0))
lost_song = Music('assets\music\lost_song.mp3')
menu_song = Music('assets\music\menu_song.mp3')
playing_song = Music('assets/music/playing_song_loop.mp3')
playing_song.file.set_volume(0.75)
final_score = Font('assets\\typography\Snake Chan.ttf', 50)

# game loop
menu_song.file.play()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #It could be sys.exit() but this is a simpler method
                
    keys_state = pygame.key.get_pressed()
    if game_state == 'MENU':
        screen.blit(grass.image, grass.rect) 
        screen.blit(logo.image, logo.rect)
        screen.blit(button_play.image, button_play.rect)
        snake.spawn()
        
        if (pygame.mouse.get_pressed()[0]):
            mouse_position = pygame.mouse.get_pos()
            if button_play.rect.collidepoint(mouse_position):
                game_state = 'PLAYING'
                menu_song.file.stop()
                playing_song.file.play(loops=-1)
                score = 0
                
    elif game_state == 'PLAYING':
        
        screen.blit(grass.image, grass.rect)
        screen.blit(snake.head_images[snake.is_moving], snake.rect)
        python.spawn()
        
        if snake.rect.colliderect(python.rect):
            score += 1
            python.switch_spawn()
            
        if snake.rect.x < 0 or snake.rect.y < 0 or snake.rect.x > 800 or snake.rect.y > 600:
            playing_song.file.stop()
            lost_song.file.play()
            game_state = 'LOST'
            
        if snake.is_moving == 'left':
            snake.move_left()
        if snake.is_moving == 'down':
            snake.move_down()
        if snake.is_moving == 'right':
            snake.move_right()    
        if snake.is_moving == 'up':
            snake.move_up()
        
        if keys_state[pygame.K_UP] or keys_state[pygame.K_w]:
            snake.is_moving = 'up'
        if keys_state[pygame.K_DOWN] or keys_state[pygame.K_s]:
            snake.is_moving = 'down'
        if keys_state[pygame.K_LEFT] or keys_state[pygame.K_a]:
            snake.is_moving = 'left'
        if keys_state[pygame.K_RIGHT] or keys_state[pygame.K_d]:
            snake.is_moving = 'right'
            
    elif game_state == 'LOST':
        final_score_surface = final_score.render(str(score), True, '#C1FD20')        
        screen.blit(death_message.image, death_message.rect)
        screen.blit(final_score_surface, (421, 488))
        screen.blit(button_play_again.image, button_play_again.rect)
        
        if (pygame.mouse.get_pressed()[0]):
            mouse_position = pygame.mouse.get_pos()
            if button_play_again.rect.collidepoint(mouse_position):
                score = 0
                snake.rect = snake.head_down.get_rect(topleft=(40, 300))
                game_state = 'PLAYING'
                lost_song.file.stop()
                playing_song.file.play(loops=-1)    
            
    pygame.display.flip()
    clock.tick(60)  

pygame.quit()