# ui.py

import pygame
from config import (
    COLOR_BUTTON,
    COLOR_BUTTON_HOVER,
    COLOR_BUTTON_TEXT,
    COLOR_BUTTON_BFS,
    COLOR_BUTTON_DFS,
    COLOR_BUTTON_BFS_HOVER,
    COLOR_BUTTON_DFS_HOVER,
)

class Button:
    def __init__(self, rect: pygame.Rect, text: str):
        self.rect = rect
        self.text = text
        self.hover = False

    def update_hover(self, mouse_pos: tuple[int, int]) -> None:
        self.hover = self.rect.collidepoint(mouse_pos)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, text: str) -> None:
        if text == "BFS":
            base_color = COLOR_BUTTON_BFS_HOVER if self.hover else COLOR_BUTTON_BFS
        elif text == "DFS":
            base_color = COLOR_BUTTON_DFS_HOVER if self.hover else COLOR_BUTTON_DFS
        else:
            base_color = COLOR_BUTTON_HOVER if self.hover else COLOR_BUTTON
            
        pygame.draw.rect(surface, base_color, self.rect, border_radius=6)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 1, border_radius=6)

        text_surf = font.render(self.text, True, COLOR_BUTTON_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
