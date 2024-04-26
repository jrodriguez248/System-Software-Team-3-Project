import pygame
from classes.world_map import world_map

# Pygame setup
pygame.init()
pygame.display.set_caption("Waterlogged")
screen = pygame.display.set_mode((500, 500))
font = pygame.font.Font('./assets/SourceCodePro-Regular.ttf', 30)

# Game setup
map = world_map()

def loop():
    screen.fill((0, 0, 0))

    map.render(screen, font)

    pygame.display.flip()


def on_key_pressed(event: pygame.event.Event):
    if event.key == pygame.K_SPACE:
        print("spacebar pressed")


def on_mouse_pressed(event: pygame.event.Event):
    left, middle, right = pygame.mouse.get_pressed()
    if left:
        print("left mouse pressed")
    if middle:
        print('middle mouse pressed')



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
