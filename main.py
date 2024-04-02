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
        new_body = [{'image': segment['image'], 'position': self.pythons[i-1]['position']} for i, segment in enumerate(self.pythons[1:], start=1)]
        
        self.pythons = [new_head] + new_body

        
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
        
    def play():
        Game.python.move()

Game = Game()
GUI = GUI()


# game loop
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

GUI.menu_song.file.play()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #It could be sys.exit() but this is a simpler method
        
        if event.type == SCREEN_UPDATE:        
            if game_state == 'MENU':
                screen.blit(GUI.grass.image, GUI.grass.rect) 
                screen.blit(GUI.logo.image, GUI.logo.rect)
                screen.blit(GUI.button_play.image, GUI.button_play.rect)
                
                if (pygame.mouse.get_pressed()[0]):
                    mouse_position = pygame.mouse.get_pos()
                    if GUI.button_play.rect.collidepoint(mouse_position):
                        game_state = 'PLAYING'
                        GUI.menu_song.file.stop()
                        GUI.playing_song.file.play(loops=-1)
                        score = 0                
                        
            elif game_state == 'PLAYING':
                screen.blit(GUI.grass.image, GUI.grass.rect)
                Game.python.spawn()
                Game.pythons.spawn()
                Game.python.move()
                
                # if python.rect.colliderect(pythons.rect):
                #     score += 1
                #     pythons.switch_spawn()
                    
                # if python.rect.x < 0 or python.rect.y < 0 or python.rect.x > 800 or python.rect.y > 600:
                #     playing_song.file.stop()
                #     lost_song.file.play()
                #     game_state = 'LOST'
                    
            elif game_state == 'LOST':
                final_score_surface = GUI.final_score.render(f'Score: {score}', True, '#C1FD20')        
                screen.blit(GUI.death_message.image, GUI.death_message.rect)
                screen.blit(final_score_surface, (421, 488))
                screen.blit(GUI.button_play_again.image, GUI.button_play_again.rect)
                
                if (pygame.mouse.get_pressed()[0]):
                    mouse_position = pygame.mouse.get_pos()
                    if GUI.button_play_again.rect.collidepoint(mouse_position):
                        score = 0
                        GUI.python.rect = GUI.python.head_down.get_rect(topleft=(40, 300))
                        game_state = 'PLAYING'
                        GUI.lost_song.file.stop()
                        GUI.playing_song.file.play(loops=-1)
                        
    # User input event loop
    keys_state = pygame.key.get_pressed()
    if game_state == 'PLAYING':
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
