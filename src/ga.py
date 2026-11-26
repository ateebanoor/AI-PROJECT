"""Lab 06: a genetic algorithm that evolves the four weights of GAAgent.

Individual  = a vector of N_FEATURES weights.
Fitness     = average of (10 * score + 0.1 * steps) over the training games:
              eating matters most, surviving longer breaks ties.
Selection   = tournament; Crossover = uniform; Mutation = Gaussian; Elitism.
"""
import json
import random

import numpy as np

import config
from agents import GAAgent
from runner import play_game


def fitness(weights, seeds=config.TRAIN_SEEDS):
    """Average game quality of one weight vector on the given seeds."""
    agent = GAAgent(weights)
    total = 0.0
    for seed in seeds:
        result = play_game(agent, seed)
        total += 10 * result.score + 0.1 * result.steps
    return total / len(seeds)


def _tournament(population, scores, rng):
    """Pick TOURNAMENT_SIZE random individuals and return the fittest."""
    picks = rng.sample(range(len(population)), config.TOURNAMENT_SIZE)
    return population[max(picks, key=lambda i: scores[i])]


def _crossover(parent_a, parent_b, rng):
    """Each weight of the child comes from a randomly chosen parent."""
    return np.array([a if rng.random() < 0.5 else b
                     for a, b in zip(parent_a, parent_b)])


def _mutate(weights, rng):
    """Add Gaussian noise to each weight with probability MUTATION_RATE."""
    child = weights.copy()
    for i in range(len(child)):
        if rng.random() < config.MUTATION_RATE:
            child[i] += rng.gauss(0, config.MUTATION_SIGMA)
    return child


def evolve(seed=config.MASTER_SEED, generations=config.GENERATIONS, verbose=True):
    """Run the GA. Returns (best_weights, history); history has one dict per generation."""
    rng = random.Random(seed)
    population = [np.array([rng.uniform(-1, 1) for _ in range(config.N_FEATURES)])
                  for _ in range(config.POP_SIZE)]
    history = []
    best_weights, best_fit = None, -np.inf

    for gen in range(generations):
        scores = [fitness(ind) for ind in population]
        order = sorted(range(len(population)), key=lambda i: scores[i], reverse=True)
        if scores[order[0]] > best_fit:
            best_fit, best_weights = scores[order[0]], population[order[0]].copy()
        history.append({"generation": gen + 1,
                        "best": max(scores),
                        "mean": float(np.mean(scores))})
        if verbose:
            print(f"  generation {gen + 1:2d}/{generations}: "
                  f"best fitness {max(scores):7.1f}, mean {np.mean(scores):7.1f}")

        # next generation: keep the elite, fill the rest with mutated children
        next_pop = [population[i].copy() for i in order[:config.ELITE_COUNT]]
        while len(next_pop) < config.POP_SIZE:
            mum = _tournament(population, scores, rng)
            dad = _tournament(population, scores, rng)
            next_pop.append(_mutate(_crossover(mum, dad, rng), rng))
        population = next_pop

    return best_weights, history


def save_weights(weights, path=config.WEIGHTS_FILE):
    with open(path, "w") as f:
        json.dump([float(w) for w in weights], f)


def load_weights(path=config.WEIGHTS_FILE):
    """Read saved weights. Raises FileNotFoundError or ValueError with a clear message."""
    try:
        with open(path) as f:
            weights = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"no trained weights at {path} - train the GA first") from None
    except json.JSONDecodeError as err:
        raise ValueError(f"weights file {path} is not valid JSON: {err}") from None
    if not isinstance(weights, list) or len(weights) != config.N_FEATURES:
        raise ValueError(f"weights file {path} must hold a list of {config.N_FEATURES} numbers")
    return np.array(weights, dtype=float)
