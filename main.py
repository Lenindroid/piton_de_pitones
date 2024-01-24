import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pitón de pitones (Alpha 1.0.2)')
clock = pygame.time.Clock()
running = True
game_state = 'MENU'

# defining classes
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets\snake\head.png').convert_alpha()
        self.rect = self.image.get_rect(center=(200, 300))
    
    def move_left(self):
        self.rect.x -= 10
    
    def move_right(self):
        self.rect.x += 10
    
    def move_up(self):
        self.rect.y += 10
    
    def move_down(self):
        self.rect.y -= 10

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

# loading images
grass = Static_Image('assets\grass.png', False, topleft = (0, 0))
logo = Static_Image('assets\logo.png', True, center = (400, 150))
button_play = Static_Image('assets\play_button.png', True, topleft = (200, 186))
snake = Snake()
death_message = Font('assets\\typography\Snake Chan.ttf', 50).render('Haz murido', True, '#C1FD20')

# game loop
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
        # flip() the display to put your work on screen
    elif game_state == 'PLAYING':
        screen.blit(grass.image, grass.rect)
        screen.blit(snake.image, snake.rect)
        
        if snake.rect.x <= 0 or snake.rect.y <= 0:
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
    clock.tick(60)  # limits FPS to 60

pygame.quit()