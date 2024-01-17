import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pitón de pitones')
clock = pygame.time.Clock()
running = True

# loading assets 
logo = pygame.image.load('assets\logo_alpha_1_0_0.png').convert()
play_button = pygame.image.load('assets\play_button.png') .convert()

# buttons positioning
button_rect = play_button.get_rect()
button_rect.center = (400, 400)

# menu functions


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #It could be sys.exit() but this is a simpler method
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #My game
            pass

    # RENDER YOUR GAME HERE
    screen.fill(('white')) 
    screen.blit(logo, (100, 100))  
    screen.blit(play_button, button_rect) 
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()