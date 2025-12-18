# main.py

import pygame
from typing import Union
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    COLOR_BG,
    COLOR_UI_BG,
    COLOR_UI_BORDER,
    UI_PANEL_HEIGHT,
)
from grid import Grid
from algorithms import BFSAnimator, DFSAnimator
from ui import Button

Animator = Union[BFSAnimator, DFSAnimator]


def stop_animation(grid: Grid, animator: Animator | None) -> Animator | None:
    grid.reset_search_state()
    return None


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Maze Visualizer")

    clock = pygame.time.Clock()
    running = True

    grid = Grid()
    animator: Animator | None = None

    font = pygame.font.SysFont(None, 24)

    buttons: list[Button] = []
    labels = ["BFS", "DFS", "Generate walls", "Clear walls", "Reset search"]
    button_width = 130
    button_height = 32
    padding = 10
    spacing = 10

    x = padding
    y = (UI_PANEL_HEIGHT - button_height) // 2

    for label in labels:
        rect = pygame.Rect(x, y, button_width, button_height)
        buttons.append(Button(rect, label))
        x += button_width + spacing

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for b in buttons:
                    b.update_hover(mouse_pos)

                x, y = mouse_pos
                buttons_state = event.buttons
                over_button = any(b.rect.collidepoint(mouse_pos) for b in buttons)

                if buttons_state[0] and not over_button:
                    animator = stop_animation(grid, animator)
                    grid.transform_to_wall(x, y)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    x, y = mouse_pos

                    clicked_button = next(
                        (b for b in buttons if b.rect.collidepoint(mouse_pos)), None
                    )

                    if clicked_button is not None:
                        label = clicked_button.text

                        if label == "BFS":
                            animator = BFSAnimator(grid)
                            animator.start_search()

                        elif label == "DFS":
                            animator = DFSAnimator(grid)
                            animator.start_search()

                        elif label == "Generate walls":
                            grid.generate_walls()
                            animator = stop_animation(grid, animator)

                        elif label == "Clear walls":
                            grid.clear_walls()
                            animator = stop_animation(grid, animator)

                        elif label == "Reset search":
                            animator = stop_animation(grid, animator)

                    else:
                        animator = stop_animation(grid, animator)
                        grid.transform_to_wall(x, y)

        if animator is not None and not animator.finished:
            animator.step()

        screen.fill(COLOR_BG)

        pygame.draw.rect(
            screen,
            COLOR_UI_BG,
            pygame.Rect(0, 0, WINDOW_WIDTH, UI_PANEL_HEIGHT),
        )
        pygame.draw.line(
            screen,
            COLOR_UI_BORDER,
            (0, UI_PANEL_HEIGHT - 1),
            (WINDOW_WIDTH, UI_PANEL_HEIGHT - 1),
            1,
        )

        for b in buttons:
            b.draw(screen, font, b.text)

        grid.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
