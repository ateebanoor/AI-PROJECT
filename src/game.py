"""The Snake environment: a Snake object and the game that enforces the rules."""
import random
from collections import deque

from config import (ACTIONS, GRID_SIZE, MAX_STEPS, START_LENGTH,
                    STARVE_LIMIT)


class Snake:
    """The snake's body. Only this class changes the body (encapsulation)."""

    def __init__(self, start, length=START_LENGTH):
        x, y = start
        # head first; the snake starts out stretched to the left, facing right
        self._body = deque((x - i, y) for i in range(length))
        self._cells = set(self._body)   # same cells as a set, for fast lookups

    @property
    def head(self):
        return self._body[0]

    @property
    def tail(self):
        return self._body[-1]

    @property
    def cells(self):
        """A copy of the occupied cells, so callers cannot change the snake."""
        return set(self._cells)

    def occupies(self, cell):
        return cell in self._cells

    def __len__(self):
        return len(self._body)

    def move(self, new_head, grow):
        """Put the head on new_head; the tail follows unless the snake grows."""
        if not grow:
            old_tail = self._body.pop()
            self._cells.discard(old_tail)
        self._body.appendleft(new_head)
        self._cells.add(new_head)


class SnakeGame:
    """One game of Snake on a size x size grid. Seeded, so it is reproducible."""

    def __init__(self, size=GRID_SIZE, seed=0):
        self.size = size
        self._rng = random.Random(seed)   # the only source of randomness
        self.snake = Snake((size // 2, size // 2))
        self.score = 0                    # food eaten
        self.steps = 0                    # moves made = survival time
        self.steps_since_food = 0
        self.alive = True
        self.death_cause = None           # "wall", "self", "starved", "timeout" or "won"
        self.food = self._place_food()

    # ---- helpers the agents may use ----
    def in_bounds(self, cell):
        x, y = cell
        return 0 <= x < self.size and 0 <= y < self.size

    def is_safe(self, cell):
        """True if the head may move onto cell now.

        The tail cell counts as safe because the tail moves away in the same
        step (unless the snake eats, and food is never on the snake).
        """
        if not self.in_bounds(cell):
            return False
        return (not self.snake.occupies(cell)) or cell == self.snake.tail

    def next_cell(self, action):
        dx, dy = ACTIONS[action]
        x, y = self.snake.head
        return (x + dx, y + dy)

    # ---- the transition function ----
    def step(self, action):
        """Apply one action ("UP", "DOWN", "LEFT" or "RIGHT")."""
        if not self.alive:
            return
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action!r}")
        new_head = self.next_cell(action)
        self.steps += 1
        self.steps_since_food += 1

        if not self.in_bounds(new_head):
            self._die("wall")
            return
        if not self.is_safe(new_head):
            self._die("self")
            return

        ate = new_head == self.food
        self.snake.move(new_head, grow=ate)
        if ate:
            self.score += 1
            self.steps_since_food = 0
            self.food = self._place_food()
            if self.food is None:             # the board is full
                self._die("won")
        elif self.steps_since_food >= STARVE_LIMIT:
            self._die("starved")
        elif self.steps >= MAX_STEPS:
            self._die("timeout")

    def _place_food(self):
        occupied = self.snake.cells
        free = [(x, y) for x in range(self.size) for y in range(self.size)
                if (x, y) not in occupied]
        return self._rng.choice(free) if free else None

    def _die(self, cause):
        self.alive = False
        self.death_cause = cause
