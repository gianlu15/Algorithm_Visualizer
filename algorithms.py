from collections import deque   # double-ended queue
from typing import Dict, Tuple,  Optional, Set

from grid import Grid
import time
# Alias
Coord = Tuple[int, int]

class BFSAnimator:

    def __init__(self, grid: Grid):
        self.grid = grid
        self.start: Coord = grid.start
        self.end: Coord = grid.end

        # next cells to be explored 
        self.queue: deque[Coord] = deque()
        
        # visited cells
        self.visited: Set[Coord] = set()
        
        # used when the path is found
        self.parent: Dict[Coord, Optional[Coord]] = {}

        self.finished: bool = False
        
        self.cell_visited_counter = 0
        self.cell_in_path_counter = 0
        self.start_time = time.perf_counter()


    def start_search(self) -> None:
        self.grid.reset_search_state()

        # clear all
        self.queue.clear()
        self.visited.clear()
        self.parent.clear()
        self.finished = False
        self.cell_visited_counter = 0
        self.cell_in_path_counter = 0
        self.start_time = time.perf_counter()

        self.queue.append(self.start)
        self.visited.add(self.start)
        self.parent[self.start] = None

        start_row, start_column = self.start
        
        # nodes that are in queue
        self.grid.cells[start_row][start_column].in_frontier = True



    def step(self) -> None:
        if self.finished:
            return

        if not self.queue:
            self.finished = True
            return

        self.cell_visited_counter += 1
        current = self.queue.popleft()
        current_row, current_column = current
        current_cell = self.grid.cells[current_row][current_column]

        current_cell.in_frontier = False
        current_cell.is_visited = True

        if current == self.end:
            elapsed = time.perf_counter() - self.start_time
            print(f"Tempo BFS: {elapsed:.4f} secondi")
            print(self.cell_visited_counter)
            self._reconstruct_path()
            print(self.cell_in_path_counter)
            self.finished = True
            return

        # find neighbors
        for neighbors_row, neighbors_columns in self.grid.neighbors(current_row, current_column):
            next = (neighbors_row, neighbors_columns)
            if next not in self.visited:
                self.visited.add(next)
                self.parent[next] = current
                self.queue.append(next)

                cell = self.grid.cells[neighbors_row][neighbors_columns]
                cell.in_frontier = True

    # reverse path construction
    def _reconstruct_path(self) -> None:
        cur: Optional[Coord] = self.end
        while cur is not None:
            r, c = cur
            cell = self.grid.cells[r][c]
            cell.in_path = True
            cur = self.parent.get(cur)
            self.cell_in_path_counter += 1
            
            
class DFSAnimator:

    def __init__(self, grid: Grid):
        self.grid = grid
        self.start: Coord = grid.start
        self.end: Coord = grid.end

        # next cells to be explored 
        self.queue: deque[Coord] = deque()
        
        # visited cells
        self.visited: Set[Coord] = set()
        
        # used when the path is found
        self.parent: Dict[Coord, Optional[Coord]] = {}

        self.finished: bool = False
        
        self.cell_visited_counter: int
        self.cell_in_path_counter: int
        self.start_time: float



    def start_search(self) -> None:
        self.grid.reset_search_state()

        # clear all
        self.queue.clear()
        self.visited.clear()
        self.parent.clear()
        self.finished = False
        self.cell_visited_counter = 0
        self.cell_in_path_counter = 0
        self.start_time = time.perf_counter()

        self.queue.append(self.start)
        self.visited.add(self.start)
        self.parent[self.start] = None

        start_row, start_column = self.start
        
        # nodes that are in queue
        self.grid.cells[start_row][start_column].in_frontier = True



    def step(self) -> None:
        
        if self.finished:
            return

        if not self.queue:
            self.finished = True
            return
           
        self.cell_visited_counter += 1
        current = self.queue.pop()
        current_row, current_column = current
        current_cell = self.grid.cells[current_row][current_column]

        current_cell.in_frontier = False
        current_cell.is_visited = True

        if current == self.end:
            elapsed = time.perf_counter() - self.start_time
            print(f"Tempo BFS: {elapsed:.4f} secondi")
            print(self.cell_visited_counter)
            self._reconstruct_path()
            print(self.cell_in_path_counter)
            self.finished = True
            return

        # find neighbors
        for neighbors_row, neighbors_columns in self.grid.neighbors(current_row, current_column):
            next = (neighbors_row, neighbors_columns)
            if next not in self.visited:
                self.visited.add(next)
                self.parent[next] = current
                self.queue.append(next)

                cell = self.grid.cells[neighbors_row][neighbors_columns]
                cell.in_frontier = True

    # reverse path construction
    def _reconstruct_path(self) -> None:
        cur: Optional[Coord] = self.end
        while cur is not None:
            r, c = cur
            cell = self.grid.cells[r][c]
            cell.in_path = True
            cur = self.parent.get(cur)
            self.cell_in_path_counter += 1