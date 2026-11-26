"""Shared settings for the Snake AI project.

Keeping every number in one place means each experiment can be reproduced
and every parameter can be explained (and changed live) during the viva.
"""
import os

# --- paths (relative to the repository root, not to where you run Python) ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURE_DIR = os.path.join(ROOT_DIR, "outputs", "figures")
RESULT_DIR = os.path.join(ROOT_DIR, "outputs", "results")
WEIGHTS_FILE = os.path.join(RESULT_DIR, "best_weights.json")

# --- game rules ---
GRID_SIZE = 10          # the board is GRID_SIZE x GRID_SIZE cells
START_LENGTH = 3        # initial snake length
STARVE_LIMIT = 100      # die after this many moves without eating (stops endless loops)
MAX_STEPS = 5000        # hard safety cap on one game

# Actions are (dx, dy). y grows downwards, as on a computer screen.
ACTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

# --- experiment ---
MASTER_SEED = 42        # seeds the genetic algorithm
N_TEST_GAMES = 100      # games per agent; game i uses seed i (same for every agent)
TRAIN_SEEDS = [1000, 1001, 1002, 1003, 1004]   # GA training games (kept apart from test seeds)

# --- genetic algorithm ---
POP_SIZE = 20           # individuals (weight vectors) per generation
GENERATIONS = 30
TOURNAMENT_SIZE = 3     # parents are the best of this many random individuals
ELITE_COUNT = 2         # best individuals copied unchanged into the next generation
MUTATION_RATE = 0.3     # probability that one weight is mutated
MUTATION_SIGMA = 0.3    # standard deviation of the Gaussian mutation
N_FEATURES = 4          # see agents.move_features

# --- viewer ---
CELL_PIXELS = 36
FPS = 12
