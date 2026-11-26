"""Play one full game with an agent and report what happened."""
from collections import namedtuple

from game import SnakeGame

# nodes_per_move is 0 for agents that do not search
GameResult = namedtuple("GameResult", "score steps cause nodes_per_move")


def play_game(agent, seed):
    """Run agent on a fresh game with this seed until the snake dies."""
    game = SnakeGame(seed=seed)
    agent.reset()
    while game.alive:
        game.step(agent.choose_move(game))
    searches = getattr(agent, "searches", 0)
    nodes = getattr(agent, "nodes_expanded", 0)
    nodes_per_move = nodes / searches if searches else 0.0
    return GameResult(game.score, game.steps, game.death_cause, nodes_per_move)
