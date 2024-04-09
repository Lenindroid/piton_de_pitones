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

pythons_assets = [
    Static_Image('assets\python\cat_python.png', True), 
    Static_Image('assets\python\gabriela_python.png', True), 
    Static_Image('assets\python\legacy_lenin.png', True)
]
        
class Python(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pythons = [{'image': Static_Image('assets\python\head.png', True).image, 'position': Vector2(3, 3)}, {'image': pythons_assets[0].image, 'position': Vector2(2, 3)}]
        self.direction = Vector2(1, 0)
        
    def spawn(self):
        for python in self.pythons:
            x_position = int(cell_size * python['position'].x)
            y_position = int(cell_size * python['position'].y)
            rect = python['image'].get_rect(topleft=(x_position, y_position))
            screen.blit(python['image'], rect)
        
    def move(self):
        new_head = {'image': self.pythons[0]['image'], 'position': self.pythons[0]['position'] + self.direction}
        self.last_position = self.pythons[-1]['position']
        new_body = [{'image': segment['image'], 'position': self.pythons[i-1]['position']} for i, segment in enumerate(self.pythons[1:], start=1)]
        self.pythons = [new_head] + new_body
        
    def push_python(self, image, position):
        self.pythons.append({'image': image, 'position': position})

        
class Pythons:
    def __init__(self): 
        self.position = Vector2(random.randint(0, cell_number_x - 1), random.randint(0, cell_number_y - 1))
        x_position = int(cell_size * self.position.x)
        y_position = int(cell_size * self.position.y)
        self.rect = pygame.rect.Rect(x_position, y_position, cell_size, cell_size)
        self.pythons_assets = ['assets\python\cat_python.png', 'assets\python\legacy_lenin.png', 'assets\python\gabriela_python.png']
        
    def spawn(self):
        self.image = pygame.image.load(self.pythons_assets[0]).convert()
        screen.blit(self.image, self.rect)
    
    def switch_spawn(self):
        random.shuffle(self.pythons_assets)
        self.position = Vector2(random.randint(0, cell_number_x - 1), random.randint(0, cell_number_y - 1))
        self.rect = pygame.rect.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
   
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
        
class GUI():
    def __init__(self):
        self.grass = Static_Image('assets\grass.png', False, topleft = (0, 0))
        self.pythons = Pythons()
        self.logo = Static_Image('assets\logo.png', True, center = (400, 150))
        self.button_play = Static_Image('assets\play_button.png', True, topleft = (200, 186))
        self.button_play_again = Static_Image('assets\play_again.png', True, topleft = (52, 488))
        self.death_message = Static_Image('assets\DEATH_MESSAGE.png', True, topleft = (0, 0))
        self.lost_song = Music('assets\music\lost_song.mp3')
        self.menu_song = Music('assets\music\menu_song.mp3')
        self.playing_song = Music('assets/music/playing_song_loop.mp3')
        self.playing_song.file.set_volume(0.75)
        self.final_score = Font('assets\\typography\Snake Chan.ttf', 50)
    
class Game():
    def __init__(self):
        self.python = Python()
        self.pythons = Pythons()
        self.score = 0
        self.state = 'MENU'
        
    def play(self):
        screen.blit(GUI.grass.image, GUI.grass.rect)
        self.python.spawn()
        self.pythons.spawn()
        self.python.move()
        
    def check_collision(self):
        if self.pythons.position == self.python.pythons[0]['position']:
            self.python.push_python(self.pythons.image, self.python.last_position)
            self.score += 1
            self.pythons.switch_spawn()
            
        if self.python.pythons[0]['position'].x < 0 or self.python.pythons[0]['position'].y < 0 or self.python.pythons[0]['position'].x > cell_number_x or self.python.pythons[0]['position'].y > cell_number_y or self.python.pythons[0]['position'] == self.python.pythons[-1]['position']:
            GUI.playing_song.file.stop()
            GUI.lost_song.file.play()
            self.state = 'LOST'
            

Game = Game()
GUI = GUI()


# game loop
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 130)

GUI.menu_song.file.play()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #It could be sys.exit() but this is a simpler method
        
        if event.type == SCREEN_UPDATE:        
            if Game.state == 'MENU':
                screen.blit(GUI.grass.image, GUI.grass.rect) 
                screen.blit(GUI.logo.image, GUI.logo.rect)
                screen.blit(GUI.button_play.image, GUI.button_play.rect)
                
                if (pygame.mouse.get_pressed()[0]):
                    mouse_position = pygame.mouse.get_pos()
                    if GUI.button_play.rect.collidepoint(mouse_position):
                        Game.state = 'PLAYING'
                        GUI.menu_song.file.stop()
                        GUI.playing_song.file.play(loops=-1)
                        Game.score = 0 #Pls, check if this is necesary              
                        
            elif Game.state == 'PLAYING':
                Game.play()
                Game.check_collision()
                    
            elif Game.state == 'LOST':
                final_score_surface = GUI.final_score.render(f'Score: {Game.score}', True, '#C1FD20')        
                screen.blit(GUI.death_message.image, GUI.death_message.rect)
                screen.blit(final_score_surface, (421, 488))
                screen.blit(GUI.button_play_again.image, GUI.button_play_again.rect)
                
                if (pygame.mouse.get_pressed()[0]):
                    mouse_position = pygame.mouse.get_pos()
                    if GUI.button_play_again.rect.collidepoint(mouse_position):
                        Game.score = 0
                        Game.python.pythons = [{'image': Static_Image('assets\python\head.png', True).image, 'position': Vector2(3, 3)}, {'image': pythons_assets[0].image, 'position': Vector2(2, 3)}]
                        Game.python.direction = Vector2(1, 0)
                        Game.state = 'PLAYING'
                        GUI.lost_song.file.stop()
                        GUI.playing_song.file.play(loops=-1)
                        
    # User input event loop
    keys_state = pygame.key.get_pressed()
    if Game.state == 'PLAYING':
        if keys_state[pygame.K_UP] or keys_state[pygame.K_w]:
            Game.python.direction = Vector2(0, -1)
        if keys_state[pygame.K_DOWN] or keys_state[pygame.K_s]:
            Game.python.direction = Vector2(0, 1)
        if keys_state[pygame.K_LEFT] or keys_state[pygame.K_a]:
           Game.python.direction = Vector2(-1, 0)
        if keys_state[pygame.K_RIGHT] or keys_state[pygame.K_d]:
           Game.python.direction = Vector2(1, 0)
    
    pygame.display.flip()
    clock.tick(60)  

pygame.quit()
