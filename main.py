import pygame
from classes.world_map import world_map

# Constants
MOVE_DELAY = 200 # Delay between movements when holding movement key (in milliseconds)

# Pygame setup
pygame.init()
pygame.display.set_caption("Waterlogged")
screen = pygame.display.set_mode((960, 680))
font = pygame.font.Font('./assets/SourceCodePro-Regular.ttf', 24)
pygame.key.set_repeat(MOVE_DELAY, MOVE_DELAY)

# Game setup
map = world_map()


def loop():
    screen.fill((0, 0, 0))

    map.render(screen, font, render_regeion=(61, 21))

    pygame.display.flip()


def on_key_pressed(event: pygame.event.Event):
    # Movement
    if event.key == pygame.K_UP:
        map.move_player('n')
    elif event.key == pygame.K_DOWN:
        map.move_player('s')
    elif event.key == pygame.K_RIGHT:
        map.move_player('e')
    elif event.key == pygame.K_LEFT:
        map.move_player('w')

    # Interaction
    elif event.key == pygame.K_e:
        letter = map.get_nearby_interactable()

        if letter == '':
            return # Exit function, because no nearby interactables were found
        elif letter == 'B':
            print('interacted with Blacksmith')
        elif letter == 'H':
            print('interacted with Inn')
        elif letter == 'S':
            print('interacted with Shop')
        elif letter == 'U':
            print('interacted with Boat')
        elif letter == 'O' or letter == 'T':
            resource = map.get_nearby_resource()

            # Make sure resource was actualy found. This shouldn't be a problem, but doesn't hurt to check.
            if (resource == None):
                print('main.py -> on_key_pressed: Warning: No resource found nearby')
                return            
            
            resource.mine(0.1)

            if resource.is_mined():
                print('Resource collected')
                map.remove_resource(resource.location)
            else:
                print('Mined resource.', resource.health, 'health remaining')
            

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
