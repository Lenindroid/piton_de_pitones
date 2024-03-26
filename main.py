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
class Static_Image (pygame.sprite.Sprite):
    def __init__(self, route, alpha, **rectangle):
        super().__init__()
        if (alpha): 
            self.image = pygame.image.load(route).convert_alpha()
        else: 
            self.image = pygame.image.load(route).convert()
            
        if rectangle:
            self.rect = self.image.get_rect(**rectangle)
        else:
            self.rect = self.image.get_rect()

pythons_assets = [Static_Image('assets\python\cat_python.png', True).image, Static_Image('assets\python\gabriela_python.png', True).image, Static_Image('assets\python\legacy_lenin.png', True).image]
        
class Python(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pythons = [{'image': Static_Image('assets\python\head.png', True).image, 'position': Vector2(3, 3)}, {'image': pythons_assets[0], 'position': Vector2(2, 3)}]
        self.direction = Vector2(1, 0)
        
    def spawn(self):
        for python in self.pythons:
            x_position = int(cell_size * python['position'].x)
            y_position = int(cell_size * python['position'].y)
            rect = python['image'].get_rect(topleft=(x_position, y_position))
            screen.blit(python['image'], rect)
        
    def move(self):
        new_head = self.pythons[0]
        new_head['position'] += self.direction
        python_moved = [new_head] + self.pythons[:-1]
        self.pythons = python_moved
        
class Pythons:
    def __init__(self):
        self.x = random.randint(0, cell_number_x - 1)
        self.y = random.randint(0, cell_number_y - 1)
        self.position = Vector2(cell_size * self.x, self.y * cell_size)
        self.rect = pygame.rect.Rect(self.position.x, self.position.y, cell_size, cell_size)
        self.pythons_assets = ['assets\python\cat_python.png', 'assets\python\legacy_lenin.png', 'assets\python\gabriela_python.png']
        
    def spawn(self):
        image = pygame.image.load(self.pythons_assets[0]).convert()
        screen.blit(image, self.position)
    
    def switch_spawn(self):
        random.shuffle(self.pythons_assets)
        self.x = random.randint(0, cell_number_x - 1)
        self.y = random.randint(0, cell_number_y - 1)
        self.position = Vector2(cell_size * self.x, self.y * cell_size)
        self.rect = pygame.rect.Rect(self.position.x, self.position.y, cell_size, cell_size)

        
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
                python.spawn()
                pythons.spawn()
                python.move()
                
                # if python.rect.colliderect(pythons.rect):
                #     score += 1
                #     pythons.switch_spawn()
                    
                # if python.rect.x < 0 or python.rect.y < 0 or python.rect.x > 800 or python.rect.y > 600:
                #     playing_song.file.stop()
                #     lost_song.file.play()
                #     game_state = 'LOST'
                    
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
            python.direction = Vector2(0, -1)
        if keys_state[pygame.K_DOWN] or keys_state[pygame.K_s]:
            python.direction = Vector2(0, 1)
        if keys_state[pygame.K_LEFT] or keys_state[pygame.K_a]:
           python.direction = Vector2(-1, 0)
        if keys_state[pygame.K_RIGHT] or keys_state[pygame.K_d]:
           python.direction = Vector2(1, 0)
    
    pygame.display.flip()
    clock.tick(60)  

pygame.quit()
