# main.py

import pygame
from typing import Union, Optional

from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    COLOR_BG,
    COLOR_UI_BG,
    COLOR_UI_BORDER,
    UI_PANEL_HEIGHT,
    GRID_LEFT,
    GRID_WIDTH
)
from grid import Grid
from algorithms import BFSAnimator, DFSAnimator
from ui import Button

Animator = Union[BFSAnimator, DFSAnimator]


def stop_animation(grid: Grid, animator: Optional[Animator]) -> Optional[Animator]:
    """Ferma l'animazione corrente e resetta solo lo stato di ricerca (non i muri)."""
    grid.reset_search_state()
    return None


def draw_stats_panel(
    surface: pygame.Surface,
    x: int,
    y: int,
    width: int,
    height: int,
    title: str,
    animator: Optional[Animator],
    font_title: pygame.font.Font,
    font_body: pygame.font.Font,
) -> None:
    """Disegna un pannello con le statistiche di un algoritmo."""
    panel_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, (25, 25, 25), panel_rect)
    pygame.draw.rect(surface, (180, 180, 180), panel_rect, 1)

    # Titolo
    title_surf = font_title.render(title, True, (255, 255, 255))
    surface.blit(title_surf, (x + 10, y + 8))

    if animator is None:
        found_text = "Found: -"
        time_text = "Time: -"
        visited_text = "Visited: -"
        path_text = "Path len: -"
    else:
        found_text = "Found: " + ("Yes" if animator.found else "No")
        time_text = (
            f"Time: {animator.elapsed_time:.4f} s"
            if animator.elapsed_time > 0
            else "Time: -"
        )
        visited_text = f"Visited: {animator.cell_visited_counter}"
        path_text = f"Path len: {animator.cell_in_path_counter}"

    lines = [found_text, time_text, visited_text, path_text]
    offset_y = 40
    line_spacing = 24

    for i, text in enumerate(lines):
        surf = font_body.render(text, True, (230, 230, 230))
        surface.blit(surf, (x + 10, y + offset_y + i * line_spacing))


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Maze Visualizer")

    clock = pygame.time.Clock()
    running = True

    grid = Grid()

    # Un solo animatore in esecuzione, ma due "istanze" per le statistiche
    animator: Optional[Animator] = None
    bfs_animator: Optional[BFSAnimator] = None
    dfs_animator: Optional[DFSAnimator] = None

    font_ui = pygame.font.SysFont(None, 24)
    font_title = pygame.font.SysFont(None, 22)
    font_body = pygame.font.SysFont(None, 18)

    # Barra superiore: bottoni
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
        # uso i colori di default definiti in Button / config
        buttons.append(Button(rect, label))
        x += button_width + spacing

    # Layout pannelli statistiche a destra (sopra il labirinto)
    stats_panel_width = WINDOW_WIDTH - (GRID_LEFT + GRID_WIDTH) - 20  # margine dx
    stats_panel_x = GRID_LEFT + GRID_WIDTH + 10
    stats_panel_height = 140
    stats_panel_y_bfs = UI_PANEL_HEIGHT + 10
    stats_panel_y_dfs = stats_panel_y_bfs + stats_panel_height + 10

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # movimento mouse: aggiornamento hover + drag muri
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for b in buttons:
                    b.update_hover(mouse_pos)

                x_mouse, y_mouse = mouse_pos
                buttons_state = event.buttons
                over_button = any(b.rect.collidepoint(mouse_pos) for b in buttons)

                # drag muro solo se tasto sinistro premuto e non siamo sui bottoni
                if buttons_state[0] and not over_button:
                    animator = stop_animation(grid, animator)
                    grid.transform_to_wall(x_mouse, y_mouse)

            # click sinistro: bottoni o muro
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    x_mouse, y_mouse = mouse_pos

                    clicked_button = next(
                        (b for b in buttons if b.rect.collidepoint(mouse_pos)), None
                    )

                    if clicked_button is not None:
                        label = clicked_button.text

                        if label == "BFS":
                            if bfs_animator is None:
                                bfs_animator = BFSAnimator(grid)
                            bfs_animator.start_search()
                            animator = bfs_animator

                        elif label == "DFS":
                            if dfs_animator is None:
                                dfs_animator = DFSAnimator(grid)
                            dfs_animator.start_search()
                            animator = dfs_animator

                        elif label == "Generate walls":
                            grid.generate_walls()
                            animator = stop_animation(grid, animator)

                        elif label == "Clear walls":
                            grid.clear_walls()
                            animator = stop_animation(grid, animator)

                        elif label == "Reset search":
                            animator = stop_animation(grid, animator)
                    else:
                        # click nel labirinto -> muro
                        animator = stop_animation(grid, animator)
                        grid.transform_to_wall(x_mouse, y_mouse)

        # step dell'animatore corrente
        if animator is not None and not animator.finished:
            animator.step()

        # sfondo
        screen.fill(COLOR_BG)

        # barra superiore UI
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

        # disegna bottoni
        for b in buttons:
            b.draw(screen, font_ui, b.text)

        # disegna griglia
        grid.draw(screen)

        # pannello BFS
        draw_stats_panel(
            screen,
            stats_panel_x,
            stats_panel_y_bfs,
            stats_panel_width,
            stats_panel_height,
            "BFS",
            bfs_animator,
            font_title,
            font_body,
        )

        # pannello DFS
        draw_stats_panel(
            screen,
            stats_panel_x,
            stats_panel_y_dfs,
            stats_panel_width,
            stats_panel_height,
            "DFS",
            dfs_animator,
            font_title,
            font_body,
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
