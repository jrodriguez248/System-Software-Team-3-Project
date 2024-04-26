import pygame
from classes.world_map import world_map

# Constants
MOVE_DELAY = 200 # Delay between movements when holding movement key (in milliseconds)

# Pygame setup
pygame.init()
pygame.display.set_caption("Waterlogged")
screen = pygame.display.set_mode((500, 500))
font = pygame.font.Font('./assets/SourceCodePro-Regular.ttf', 30)
pygame.key.set_repeat(MOVE_DELAY, MOVE_DELAY)

# Game setup
map = world_map()
last_move_time = 0 # Milliseconds since last movement
holding_move_key = False # True if the player is holding down one of the arrow keys


def loop():
    screen.fill((0, 0, 0))

    map.render(screen, font)

    pygame.display.flip()


def on_key_pressed(event: pygame.event.Event):
    if event.key == pygame.K_UP:
        map.move_player('n')
    elif event.key == pygame.K_DOWN:
        map.move_player('s')
    elif event.key == pygame.K_RIGHT:
        map.move_player('e')
    elif event.key == pygame.K_LEFT:
        map.move_player('w')


def on_mouse_pressed(event: pygame.event.Event):
    if event.button == 1: # Left mouse button
        print("left mouse button pressed")


# Renders text onto the screen
def text(screen: pygame.Surface, message: str, position: tuple[int, int], size: int = 10, color: tuple[int, int, int] = (255, 255, 255)):
    
    img = font.render(message, True, color)
    screen.blit(img, position)


if __name__ == '__main__':
    exit = False
    while exit == False:
        loop()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                on_key_pressed(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                on_mouse_pressed(event)
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit = True
