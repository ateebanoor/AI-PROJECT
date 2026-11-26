"""Unit tests. Run from the repository root:  python -m unittest discover tests"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agents import AStarAgent, BFSAgent, GAAgent   # noqa: E402
from game import SnakeGame                          # noqa: E402
from ga import load_weights                         # noqa: E402
from runner import play_game                        # noqa: E402
from search import astar, bfs                       # noqa: E402


class GameTests(unittest.TestCase):
    def test_wall_kills(self):
        game = SnakeGame(seed=1)
        for _ in range(20):
            game.step("UP")
        self.assertFalse(game.alive)
        self.assertEqual(game.death_cause, "wall")

    def test_unknown_action_rejected(self):
        with self.assertRaises(ValueError):
            SnakeGame(seed=1).step("JUMP")

    def test_same_seed_same_game(self):
        self.assertEqual(SnakeGame(seed=7).food, SnakeGame(seed=7).food)


class SearchTests(unittest.TestCase):
    def test_bfs_and_astar_find_equal_cost_paths(self):
        for seed in range(30):
            game = SnakeGame(seed=seed)
            b = bfs(game, game.snake.head, game.food)
            a = astar(game, game.snake.head, game.food)
            self.assertEqual(b.cost, a.cost)          # A* is optimal, like BFS
            self.assertLessEqual(a.expanded, b.expanded + 1)

    def test_no_path_returns_none(self):
        game = SnakeGame(seed=1)
        result = bfs(game, game.snake.head, (-5, -5))   # goal outside the board
        self.assertIsNone(result.path)
        self.assertIsNone(astar(game, game.snake.head, (-5, -5)).path)


class AgentTests(unittest.TestCase):
    def test_agents_finish_games(self):
        for agent in (BFSAgent(), AStarAgent(), GAAgent([1, 1, 0.5, 0.5])):
            result = play_game(agent, seed=3)
            self.assertGreaterEqual(result.score, 0)

    def test_results_are_reproducible(self):
        self.assertEqual(play_game(AStarAgent(), 5), play_game(AStarAgent(), 5))

    def test_wrong_number_of_weights(self):
        with self.assertRaises(ValueError):
            GAAgent([1, 2])


class FileTests(unittest.TestCase):
    def test_missing_weights_file(self):
        with self.assertRaises(FileNotFoundError):
            load_weights("/no/such/file.json")

    def test_corrupt_weights_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write("not json")
        try:
            with self.assertRaises(ValueError):
                load_weights(f.name)
        finally:
            os.remove(f.name)


if __name__ == "__main__":
    unittest.main()
