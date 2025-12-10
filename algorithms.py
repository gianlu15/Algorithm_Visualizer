from collections import deque   # double-ended queue
from typing import Dict, Tuple, List, Optional

from grid import Grid

# Alias
Coord = Tuple[int, int]

def bfs_find_path(grid: Grid) -> List[Coord]:
    start: Coord = grid.start
    end: Coord = grid.end

    # next cells to be explored 
    queue = deque([start])
    
    # visited cells
    visited: Dict[Coord, bool] = {start: True}
    
    # used when the path is found
    parent: Dict[Coord, Optional[Coord]] = {start: None}

    while queue:
        current = queue.popleft()
        if current == end:
            break

        current_row, current_column = current
        for neighboirs_row, neighboirs_row in grid.neighbors(current_row, current_column):
            next = (neighboirs_row, neighboirs_row)
            if next not in visited:
                visited[next] = True
                parent[next] = current
                queue.append(next)

    # if there isn't path
    if end not in parent:
        return []

    # reverse path construction
    path: List[Coord] = []
    cur: Optional[Coord] = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]

    path.reverse()
    return path
