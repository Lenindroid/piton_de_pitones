import pygame
import random

# pygame setup
pygame.init()
cell_size = 40
cell_number_x = 20
cell_number_y = 15
screen = pygame.display.set_mode((cell_size * cell_number_x, cell_size * cell_number_y))
pygame.display.set_caption('Pitón de pitones (Alpha 1.0.7)')
clock = pygame.time.Clock()
running = True
game_state = 'MENU'

# defining classes
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        head_down = pygame.image.load('assets\snake\head.png').convert_alpha()
        self.head_images = {
        'down': head_down,
        'left': pygame.transform.rotozoom(head_down, 90),
        'right': pygame.transform.rotozoom(head_down, 270),
        'up': pygame.transform.rotozoom(head_down, 180)
        }

        self.pythons_assets = [self.head_images['down']]
        self.rect = head_down.get_rect(topleft=(0, 300))
    
    def move_left(self):
        self.rect.x -= 10
    
    def move_right(self):
        self.rect.x += 10
    
    def move_up(self):
        self.rect.y -= 10
    
    def move_down(self):
        self.rect.y += 10

class Python:
    def __init__(self):
        self.x = random.randint(0, cell_number_x - 1)
        self.y = random.randint(0, cell_number_y - 1)
        self.position = pygame.math.Vector2(cell_size * self.x, self.y * 5)
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
        self.position = pygame.math.Vector2(cell_size * self.x, self.y * 5)
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
snake = Snake()
python = Python()
death_message = Font('assets\\typography\Snake Chan.ttf', 50).render('Haz murido', True, '#C1FD20')
lost_song = Music('assets\music\lost_song.mp3')
menu_song = Music('assets\music\menu_song.mp3')
playing_song = Music('assets/music/playing_song_loop.mp3')
playing_song.file.set_volume(0.75)

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
        if (pygame.mouse.get_pressed()[0]):
            mouse_position = pygame.mouse.get_pos()
            if button_play.rect.collidepoint(mouse_position):
                game_state = 'PLAYING'
                menu_song.file.stop()
                playing_song.file.play(loops=-1)
    elif game_state == 'PLAYING':
        screen.blit(grass.image, grass.rect)
        screen.blit(snake.image, snake.rect)
        python.spawn()
        if snake.rect.colliderect(python.rect):
            python.switch_spawn()
        if snake.rect.x < 0 or snake.rect.y < 0 or snake.rect.x > 800 or snake.rect.y > 600:
            playing_song.file.stop()
            lost_song.file.play()
            game_state = 'LOST'
        if keys_state[pygame.K_UP] or keys_state[pygame.K_w]:
            snake.move_up()
        if keys_state[pygame.K_DOWN] or keys_state[pygame.K_s]:
            snake.move_down()
        if keys_state[pygame.K_LEFT] or keys_state[pygame.K_a]:
            snake.move_left()
        if keys_state[pygame.K_RIGHT] or keys_state[pygame.K_d]:
            snake.move_right()
            
    elif game_state == 'LOST':        
        screen.blit(death_message, (200, 300))
            
            
    pygame.display.flip()
    clock.tick(60)  

pygame.quit()