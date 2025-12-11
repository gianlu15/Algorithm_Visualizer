import pygame

from typing import Union
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG
from grid import Grid
from algorithms import BFSAnimator, DFSAnimator

Animator = Union[BFSAnimator, DFSAnimator]

def stop_animation(grid: Grid, animator: Animator | None) -> Animator | None:
    grid.reset_search_state()
    return None

def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption = ("Screen Demo")

    clock = pygame.time.Clock()
    running = True

    grid = Grid()
    
    animator: Animator | None = None

    while running:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                
    
             # trasform cells to wall
            elif event.type == pygame.MOUSEMOTION:              
                x, y = event.pos      
                buttons = event.buttons
                
                if buttons[0]:
                    animator = stop_animation(grid, animator)
                    grid.trasform_to_wall(x,y)

                
            # trasform cells to wall
            elif event.type == pygame.MOUSEBUTTONDOWN:
                animator = stop_animation(grid, animator)
                x, y = event.pos
                grid.trasform_to_wall(x,y)
                
                
            elif event.type == pygame.KEYDOWN:
                
               # press B to watch BFS 
               if event.key == pygame.K_b:
                    animator = BFSAnimator(grid)
                    animator.start_search()
                
                # press D to watch DFS 
               elif event.key == pygame.K_d:
                    animator = DFSAnimator(grid)
                    animator.start_search()
                 
               # press R to reset   
               elif event.key == pygame.K_r:
                    animator = stop_animation(grid, animator)
                
                # press W to reset walls   
               elif event.key == pygame.K_w:
                    grid.clear_walls()
                    animator = stop_animation(grid, animator)
                
                
        if animator is not None and not animator.finished:
            animator.step()

        screen.fill(COLOR_BG)
        grid.draw(screen)

        pygame.display.flip()
        clock.tick(60)  

    pygame.quit()
    

if __name__ == "__main__":
    main()