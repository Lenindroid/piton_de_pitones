import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pitón de pitones (Alpha 1.0.1)')
clock = pygame.time.Clock()
running = True

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

# loading images
grass = Static_Image('assets\grass.png', False, topleft=(0, 0))
logo = Static_Image('assets\logo.png', True, center=(400, 150))
button_play = Static_Image('assets\play_button.png', True, topleft=(200, 186))


# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #It could be sys.exit() but this is a simpler method
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #My game
            pass

    # RENDER YOUR GAME HERE
    screen.blit(grass.image, grass.rect) 
    screen.blit(logo.image, logo.rect)
    screen.blit(button_play.image, button_play.rect)
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()