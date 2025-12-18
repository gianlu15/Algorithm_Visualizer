import pygame
import random
from config import GRID_COLS, GRID_ROWS, CELL_HEIGHT, CELL_WIDTH, COLOR_GRID_LINES, COLOR_CELL_EMPTY, COLOR_CELL_PATH, COLOR_CELL_START, COLOR_CELL_END, COLOR_CELL_WALL,COLOR_CELL_FRONTIER,COLOR_CELL_VISITED
from typing import List, Tuple


class Cell:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        
        # maze structure
        self.is_wall = False
        
        # pathfinding
        self.is_start = False
        self.is_end = False
        self.is_visited = False
        self.in_frontier = False
        self.in_path = False

    @property
    def rect(self) -> pygame.Rect:
        x = self.col * CELL_WIDTH
        y = self.row * CELL_HEIGHT
        return pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)

    
    def reset_cell_search_state(self) -> None:
        self.is_visited = False
        self.in_frontier = False
        self.in_path = False
    

    def draw(self, surface: pygame.Surface) -> None:
        color = COLOR_CELL_EMPTY
      
         # path > start/end > wall > visited/frontier > empty
        if self.in_path:
            color = COLOR_CELL_PATH
        elif self.is_start:
            color = COLOR_CELL_START
        elif self.is_end:
            color = COLOR_CELL_END
        elif self.is_wall:
            color = COLOR_CELL_WALL
        elif self.in_frontier:
            color = COLOR_CELL_FRONTIER
        elif self.is_visited:
            color = COLOR_CELL_VISITED
        else:
            color = COLOR_CELL_EMPTY
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
        
        # fixed start and ending
        self.start = (0, 0)
        self.end = (rows - 5, cols - 2)
        self._apply_start_end()

    def _apply_start_end(self) -> None:
        sr, sc = self.start
        er, ec = self.end
        self.cells[sr][sc].is_start = True
        self.cells[er][ec].is_end = True
        
    def reset_search_state(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.reset_cell_search_state()


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
                COLOR_GRID_LINES,
                (x, 0),
                (x, self.rows * CELL_HEIGHT),
                1,
            )

        for r in range(self.rows + 1):
            y = r * CELL_HEIGHT
            pygame.draw.line(
                surface,
                COLOR_GRID_LINES,
                (0, y),
                (self.cols * CELL_WIDTH, y),
                1,
            )
    
    # find neighbors (up/down/right/left) which are not walls
    def neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        result: List[Tuple[int, int]] = []
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if not self.cells[nr][nc].is_wall:
                    result.append((nr, nc))

        return result
    
    
    def trasform_to_wall(self, x: int, y: int) -> None:
        col = x // CELL_WIDTH
        row = y // CELL_HEIGHT
        
        # check if its in the grid
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return

        cell = self.cells[row][col]

        # check if its not start or end
        if cell.is_start or cell.is_end:
            return
        
        cell.is_wall = True
     
        
    def clear_walls(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.is_wall = False
                
    def generate_walls(self) -> None:
        self.clear_walls()
        for row in self.cells:
            for cell in row:
                if not (cell.is_start or cell.is_end):
                    cell.is_wall = random.random() < 0.3