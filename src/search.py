"""Lab 04 and Lab 05: BFS and A*, written from scratch (no search libraries).

Both searches find the cheapest list of actions that takes the snake's head
to the food. The snake's body is treated as a fixed wall, and every move
costs 1, so path cost = number of moves.
"""
import heapq
from collections import deque, namedtuple

from config import ACTIONS

# path: list of action names (None if there is no path); cost: len(path);
# expanded: how many nodes the search expanded (our measure of search effort).
SearchResult = namedtuple("SearchResult", "path cost expanded")


def neighbours(game, cell):
    """Yield (action, next_cell) for every safe move from cell."""
    x, y = cell
    for action, (dx, dy) in ACTIONS.items():
        nxt = (x + dx, y + dy)
        if game.is_safe(nxt):
            yield action, nxt


def manhattan(a, b):
    """Heuristic h(n): grid distance ignoring the body.

    Admissible: every move changes x or y by exactly 1, so at least
    |dx| + |dy| moves are always needed - h never overestimates.
    Consistent too: one move changes h by at most 1, which equals its cost.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _build_path(parent, goal):
    """Walk back from goal to the start using the parent links."""
    path = []
    cell = goal
    while parent[cell] is not None:
        cell, action = parent[cell]
        path.append(action)
    path.reverse()
    return path


def bfs(game, start, goal):
    """Breadth-first search: expands the closest cells first.

    frontier = FIFO queue (deque); explored = set of cells already expanded;
    parent = dict that also remembers which cells were ever put on the frontier.
    """
    frontier = deque([start])
    explored = set()
    parent = {start: None}
    expanded = 0
    while frontier:
        cell = frontier.popleft()
        explored.add(cell)
        expanded += 1
        if cell == goal:
            path = _build_path(parent, goal)
            return SearchResult(path, len(path), expanded)
        for action, nxt in neighbours(game, cell):
            if nxt not in parent:              # not seen before
                parent[nxt] = (cell, action)
                frontier.append(nxt)
    return SearchResult(None, None, expanded)


def astar(game, start, goal):
    """A* search: expands the cell with the lowest f = g + h first.

    frontier = priority queue (heapq) of (f, h, counter, cell);
    explored = set of expanded cells; g = cheapest known cost to each cell.
    Ties on f are broken by smaller h, so the search keeps heading to the goal.
    """
    counter = 0                                # last tie-breaker: insertion order
    frontier = [(manhattan(start, goal), manhattan(start, goal), counter, start)]
    explored = set()
    g = {start: 0}
    parent = {start: None}
    expanded = 0
    while frontier:
        _, _, _, cell = heapq.heappop(frontier)
        if cell in explored:                   # stale duplicate entry
            continue
        explored.add(cell)
        expanded += 1
        if cell == goal:
            path = _build_path(parent, goal)
            return SearchResult(path, len(path), expanded)
        for action, nxt in neighbours(game, cell):
            new_g = g[cell] + 1
            if nxt not in explored and new_g < g.get(nxt, float("inf")):
                g[nxt] = new_g
                parent[nxt] = (cell, action)
                h = manhattan(nxt, goal)
                counter += 1
                heapq.heappush(frontier, (new_g + h, h, counter, nxt))
    return SearchResult(None, None, expanded)
