import pygame
from classes.world_map import world_map

# Constants
MOVE_DELAY = 200 # Delay between player movements when holding down an arrow key (in milliseconds)

# Pygame setup
pygame.init() # setup pygame
screen = pygame.display.set_mode((960, 680)) # create a window
pygame.display.set_caption("Waterlogged") # set window name
font = pygame.font.Font('./assets/SourceCodePro-Regular.ttf', 24) # create a font that we can use to draw text
pygame.key.set_repeat(MOVE_DELAY, MOVE_DELAY) # set repeat rate for keys. that way players can move by holding down the arrow keys

# Game setup
map = world_map()


def loop():
    screen.fill((0, 0, 0)) # background

    map.render(screen, font, render_regeion=(61, 21)) # draw map on screen

    pygame.display.flip() # render everything we've done


def on_key_pressed(event: pygame.event.Event):
    # Player movement
    if event.key == pygame.K_UP:
        map.move_player('n')
    elif event.key == pygame.K_DOWN:
        map.move_player('s')
    elif event.key == pygame.K_RIGHT:
        map.move_player('e')
    elif event.key == pygame.K_LEFT:
        map.move_player('w')

    # Object interaction
    elif event.key == pygame.K_e:
        letter = map.get_nearby_interactable() # look for a nearby object to interact with

        if letter == '': # nothing interactable nearby, so do nothing
            return
        
        elif letter == 'B': # blacksmith
            print('interacted with Blacksmith')
        
        elif letter == 'H': # inn
            print('interacted with Inn')
        
        elif letter == 'S': # shop
            print('interacted with Shop')
        
        elif letter == 'U': # boat
            print('interacted with Boat')
        
        elif letter == 'O' or letter == 'T': # resource
            resource = map.get_nearby_resource() # get resource attributes (health and type)
            
            resource.mine(0.1) # partially mine the resource

            if resource.is_mined():
                print('Resource collected')
                map.remove_resource(resource.location)
            else:
                print('Mined resource.', resource.health, 'health remaining')
            

def on_mouse_pressed(event: pygame.event.Event):
    # example mouse interaction code
    if event.button == 1: # Left mouse button
        print("left mouse button pressed")


if __name__ == '__main__':
    # Run gameplay loop until the game window is closed
    exit = False
    while exit == False:
        loop()

        # Handle input events (like key presses or mouse presses)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                on_key_pressed(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                on_mouse_pressed(event)
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit = True
