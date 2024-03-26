import pygame, random
from pygame.math import Vector2

# pygame setup
pygame.init()
cell_size = 40
cell_number_x = 20
cell_number_y = 15
screen = pygame.display.set_mode((cell_size * cell_number_x, cell_size * cell_number_y))
pygame.display.set_caption('Pitón de pitones (Alpha 1.1.3)')
clock = pygame.time.Clock()
running = True
game_state = 'MENU'
score = 0

# defining classes
class Python(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.head_down = pygame.image.load('assets\python\head.png').convert_alpha()
        self.head_images = {
        'down': self.head_down,
        'left': pygame.transform.rotozoom(self.head_down, 270, 1),
        'right': pygame.transform.rotozoom(self.head_down, 90, 1),
        'up': pygame.transform.rotozoom(self.head_down, 180, 1)
        }

        self.pythons_assets = [self.head_images['down']]
        self.rect = self.head_down.get_rect(topleft=(40, 300))
        self.pythons = [{'image': self.head_images['down'], 'position': Vector2(3, 3)}, {'image': self.head_images['down'], 'position': Vector2(2, 3)}]
        self.is_moving = 'right'
        
    def spawn(self):
        for python in self.pythons:
            x_position = int(cell_size * python['position'].y)
            y_position = int(cell_size * python['position'].x)
            rect = python['image'].get_rect(topleft=(x_position, y_position))
            screen.blit(python['image'], rect)
        
    def move_left(self):
        self.rect.x -= 20
    
    def move_right(self):
        self.rect.x += 20
    
    def move_up(self):
        self.rect.y -= 20
    
    def move_down(self):
        self.rect.y += 20
        
    def move(self, direction='right'):
        movement_vector = Vector2(0, 1)
        new_head_position = self.pythons[0]['position'] + movement_vector
        new_head = {'image': self.head_images[direction], 'position': new_head_position}
        python_moved = [new_head] + self.pythons[:-1]
        self.pythons = python_moved
        
class Pythons:
    def __init__(self):
        self.x = random.randint(0, cell_number_x - 1)
        self.y = random.randint(0, cell_number_y - 1)
        self.position = Vector2(cell_size * self.x, self.y * 5)
        self.rect = pygame.rect.Rect(self.position.x, self.position.y, cell_size, cell_size)
        self.should_spawn = True
        self.pythons_assets = ['assets\python\cat_python.png', 'assets\python\legacy_lenin.png', 'assets\python\gabriela_python.png']
        
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
python = Python()
pythons = Pythons()
death_message = Static_Image('assets\DEATH_MESSAGE.png', True, topleft = (0, 0))
lost_song = Music('assets\music\lost_song.mp3')
menu_song = Music('assets\music\menu_song.mp3')
playing_song = Music('assets/music/playing_song_loop.mp3')
playing_song.file.set_volume(0.75)
final_score = Font('assets\\typography\Snake Chan.ttf', 50)

# game loop
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

menu_song.file.play()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #It could be sys.exit() but this is a simpler method
        
        if event.type == SCREEN_UPDATE:        
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
                        score = 0
                        
            elif game_state == 'PLAYING':
                
                screen.blit(grass.image, grass.rect)
                screen.blit(python.head_images[python.is_moving], python.rect)
                pythons.spawn()
                
                if python.rect.colliderect(pythons.rect):
                    score += 1
                    pythons.switch_spawn()
                    
                if python.rect.x < 0 or python.rect.y < 0 or python.rect.x > 800 or python.rect.y > 600:
                    playing_song.file.stop()
                    lost_song.file.play()
                    game_state = 'LOST'
                    
                if python.is_moving == 'left':
                    python.move_left()
                if python.is_moving == 'down':
                    python.move_down()
                if python.is_moving == 'right':
                    python.move()    
                if python.is_moving == 'up':
                    python.move_up()
                    
            elif game_state == 'LOST':
                final_score_surface = final_score.render(f'Score: {score}', True, '#C1FD20')        
                screen.blit(death_message.image, death_message.rect)
                screen.blit(final_score_surface, (421, 488))
                screen.blit(button_play_again.image, button_play_again.rect)
                
                if (pygame.mouse.get_pressed()[0]):
                    mouse_position = pygame.mouse.get_pos()
                    if button_play_again.rect.collidepoint(mouse_position):
                        score = 0
                        python.rect = python.head_down.get_rect(topleft=(40, 300))
                        game_state = 'PLAYING'
                        lost_song.file.stop()
                        playing_song.file.play(loops=-1)
                        
    # User input event loop
    keys_state = pygame.key.get_pressed()
    if game_state == 'PLAYING':
        if keys_state[pygame.K_UP] or keys_state[pygame.K_w]:
            python.is_moving = 'up'
        if keys_state[pygame.K_DOWN] or keys_state[pygame.K_s]:
            python.is_moving = 'down'
        if keys_state[pygame.K_LEFT] or keys_state[pygame.K_a]:
            python.is_moving = 'left'
        if keys_state[pygame.K_RIGHT] or keys_state[pygame.K_d]:
            python.is_moving = 'right'
    
    pygame.display.flip()
    clock.tick(60)  

pygame.quit()
