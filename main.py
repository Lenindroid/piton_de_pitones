import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pitón de pitones (Alpha 1.0.2)')
clock = pygame.time.Clock()
running = True
game_active = False

# defining classes
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets\snake\head.png').convert_alpha()
        self.rect = self.image.get_rect(center=(400, 300))

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
        self.rect = self.image.get_rect(center=(400, 300))
        
    def render (self, text, AA, color):
        text_sufrace = self.font_config.render(text, AA, color)
        return text_sufrace

# loading images
grass = Static_Image('assets\grass.png', False, topleft = (0, 0))
logo = Static_Image('assets\logo.png', True, center = (400, 150))
button_play = Static_Image('assets\play_button.png', True, topleft = (200, 186))

enigma_code = Font('assets\\typography\Snake Chan.ttf', 50).render('Hello world', True, '#C1FD20')

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #It could be sys.exit() but this is a simpler method
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if button_play.rect.collidepoint(mouse_position):
                game_active = True

    if game_active == False:
        screen.blit(grass.image, grass.rect) 
        screen.blit(logo.image, logo.rect)
        screen.blit(button_play.image, button_play.rect)
        # flip() the display to put your work on screen
    else:
        screen.blit(grass.image, grass.rect)
        screen.blit(enigma_code, (400, 300))
            
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()