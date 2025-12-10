import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG
from grid import Grid
from algorithms import bfs_find_path


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption = ("Screen Demo")

    clock = pygame.time.Clock()
    running = True

    grid = Grid()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    grid.reset_search_state()

                if event.key == pygame.K_SPACE:
                    grid.reset_search_state()

                    path = bfs_find_path(grid)

                    # color path
                    for (cell_row, cell_column) in path:
                        cell = grid.cells[cell_row][cell_column]
                        cell.in_path = True
                        cell.is_visited = True 

        screen.fill(COLOR_BG)
        grid.draw(screen)

        pygame.display.flip()
        clock.tick(60)  

    pygame.quit()

if __name__ == "__main__":
    main()