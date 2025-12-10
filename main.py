import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG
from grid import Grid
from algorithms import BFSAnimator, DFSAnimator


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption = ("Screen Demo")

    clock = pygame.time.Clock()
    running = True

    grid = Grid()
    
    bfs_animator: BFSAnimator | None = None
    dfs_animator: DFSAnimator | None = None


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                
               # press B to watch BFS 
               if event.key == pygame.K_b:
                    bfs_animator = BFSAnimator(grid)
                    bfs_animator.start_search()
                
                # press D to watch DFS 
               elif event.key == pygame.K_d:
                    bfs_animator = DFSAnimator(grid)
                    bfs_animator.start_search()
                 
               # press R to reset   
               elif event.key == pygame.K_r:
                    grid.reset_search_state()
                    bfs_animator = None
                
        if bfs_animator is not None and not bfs_animator.finished:
            bfs_animator.step()

        screen.fill(COLOR_BG)
        grid.draw(screen)

        pygame.display.flip()
        clock.tick(60)  

    pygame.quit()

if __name__ == "__main__":
    main()