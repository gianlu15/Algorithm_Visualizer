import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT

def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption = ("Screen Demo")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("purple")
        pygame.display.flip()
        clock.tick(60)  

    pygame.quit()

if __name__ == "__main__":
    main()