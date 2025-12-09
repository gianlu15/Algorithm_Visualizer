import pygame
from config import GRID_COLS, GRID_ROWS, CELL_HEIGHT, CELL_WIDTH


class Cell:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.is_wall = False

    @property
    def rect(self) -> pygame.Rect:
        x = self.col * CELL_WIDTH
        y = self.row * CELL_HEIGHT
        return pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)

    def draw(self, surface: pygame.Surface) -> None:
        color = "gray"
        if self.is_wall:
            color = "blue"
        pygame.draw.rect(surface, color, self.rect)


class Grid:
    def __init__(self, rows: int = GRID_ROWS, cols: int = GRID_COLS):
        self.rows = rows
        self.cols = cols
        
        # cells matrix
        self.cells = []
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(Cell(r, c))
            self.cells.append(row)


    def draw(self, surface: pygame.Surface) -> None:
        
        # draw cells
        for row in self.cells:
            for cell in row:
                cell.draw(surface)

        # draw lines
        for c in range(self.cols + 1):
            x = c * CELL_WIDTH
            pygame.draw.line(
                surface,
                "green",
                (x, 0),
                (x, self.rows * CELL_HEIGHT),
                1,
            )

        for r in range(self.rows + 1):
            y = r * CELL_HEIGHT
            pygame.draw.line(
                surface,
                "green",
                (0, y),
                (self.cols * CELL_WIDTH, y),
                1,
            )
