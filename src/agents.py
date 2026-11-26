"""The three snake agents. All are goal-/utility-based agents (Lab 03).

Agent            <- base class: choose_move() is overridden by every subclass
 |- PathAgent    <- plans a path to the food; find_path() is overridden
 |   |- BFSAgent
 |   |- AStarAgent
 |- GAAgent      <- scores each move with a weighted rule (weights come from the GA)
"""
import numpy as np

from config import ACTIONS, N_FEATURES
from search import astar, bfs, manhattan, neighbours


class Agent:
    """Base class. An agent looks at the game (percept) and returns an action."""

    name = "Agent"

    def reset(self):
        """Called before every game."""

    def choose_move(self, game):
        raise NotImplementedError("subclasses must implement choose_move")

    @staticmethod
    def any_safe_move(game):
        """First safe action; if there is none, the snake is trapped, so any move."""
        for action in ACTIONS:
            if game.is_safe(game.next_cell(action)):
                return action
        return "UP"


class PathAgent(Agent):
    """Searches for the shortest path to the food and takes its first step.

    It re-plans every move (the food may move, the body changes). It only
    chases food: it never checks whether the move leaves the snake room to live.
    """

    name = "PathAgent"

    def __init__(self):
        self.nodes_expanded = 0   # total search effort in this game
        self.searches = 0         # number of searches in this game

    def reset(self):
        self.nodes_expanded = 0
        self.searches = 0

    def find_path(self, game, start, goal):
        raise NotImplementedError("subclasses choose the search algorithm")

    def choose_move(self, game):
        result = self.find_path(game, game.snake.head, game.food)
        self.nodes_expanded += result.expanded
        self.searches += 1
        if result.path:
            return result.path[0]
        return self.any_safe_move(game)   # no path to the food: just survive a step


class BFSAgent(PathAgent):
    name = "BFS"

    def find_path(self, game, start, goal):          # overridden method
        return bfs(game, start, goal)


class AStarAgent(PathAgent):
    name = "A*"

    def find_path(self, game, start, goal):          # overridden method
        return astar(game, start, goal)


def reachable_cells(game, start):
    """Flood fill: how many cells can be reached from start without crossing the body."""
    seen = {start}
    stack = [start]
    while stack:
        cell = stack.pop()
        for _, nxt in neighbours(game, cell):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return len(seen)


def move_features(game, action):
    """Four numbers that describe how good one move looks.

    0. safe      1 if the move does not hit a wall or the body, else 0
    1. closer    +1 if the move gets closer to the food, -1 if further
    2. space     fraction of the board still reachable after the move
    3. exits     safe neighbours of the new cell, divided by 3
    An unsafe move gets all zeros (there is no cell to look at).
    """
    new = game.next_cell(action)
    if not game.is_safe(new):
        return np.zeros(N_FEATURES)
    closer = manhattan(game.snake.head, game.food) - manhattan(new, game.food)
    space = reachable_cells(game, new) / (game.size * game.size)
    exits = sum(1 for _ in neighbours(game, new)) / 3
    return np.array([1.0, closer, space, exits])


class GAAgent(Agent):
    """Picks the move with the highest score = weights . features."""

    name = "GA"

    def __init__(self, weights):
        weights = np.asarray(weights, dtype=float)
        if weights.shape != (N_FEATURES,):
            raise ValueError(f"expected {N_FEATURES} weights, got shape {weights.shape}")
        self.weights = weights

    def choose_move(self, game):
        best_action, best_score = None, -np.inf
        for action in ACTIONS:
            score = float(self.weights @ move_features(game, action))
            if score > best_score:             # ties keep the first action
                best_action, best_score = action, score
        return best_action
