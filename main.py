import pygame


pygame.init()
pygame.display.set_caption("Waterlogged")
screen = pygame.display.set_mode((500, 500))
font = pygame.font.Font('./assets/SourceCodePro-Regular.ttf', 50)


def loop():
    screen.fill((0, 0, 0))

    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 19, 39))

    text = font.render('test string', True, (255, 255, 255))
    screen.blit(text, (mouse_pos[0], mouse_pos[1]))

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
