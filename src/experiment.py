"""Train the GA, compare the three snakes on 100 identical games, save tables and charts.

Run from the repository root:   python src/experiment.py
Everything is seeded, so the numbers are the same on every run.
"""
import csv
import os

import matplotlib
matplotlib.use("Agg")                  # draw to files; no window needed
import matplotlib.pyplot as plt
import numpy as np

import config
from agents import AStarAgent, BFSAgent, GAAgent
from ga import evolve, save_weights
from runner import play_game

CAUSES = ["wall", "self", "starved", "timeout", "won"]
COLOURS = {"BFS": "#4c78a8", "A*": "#f58518", "GA": "#54a24b"}


def evaluate_agent(agent, n_games=config.N_TEST_GAMES):
    """Play games with seeds 0..n_games-1 (the same instances for every agent)."""
    return [play_game(agent, seed) for seed in range(n_games)]


def summarise(results):
    """One row of the results table."""
    scores = np.array([r.score for r in results])
    steps = np.array([r.steps for r in results])
    return {
        "avg_score": scores.mean(),
        "std_score": scores.std(),
        "max_score": int(scores.max()),
        "avg_survival": steps.mean(),
        "std_survival": steps.std(),
        "avg_nodes_per_move": float(np.mean([r.nodes_per_move for r in results])),
        "causes": {c: sum(1 for r in results if r.cause == c) for c in CAUSES},
    }


def save_table(rows):
    """Write the results table as CSV and Markdown."""
    os.makedirs(config.RESULT_DIR, exist_ok=True)
    header = ["Agent", "Avg score", "Std score", "Max score", "Avg survival (steps)",
              "Std survival", "Avg nodes expanded / move"]
    body = []
    for name, s in rows.items():
        nodes = f"{s['avg_nodes_per_move']:.1f}" if name != "GA" else "-"
        body.append([name, f"{s['avg_score']:.2f}", f"{s['std_score']:.2f}", s["max_score"],
                     f"{s['avg_survival']:.1f}", f"{s['std_survival']:.1f}", nodes])
    with open(os.path.join(config.RESULT_DIR, "results_table.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(body)
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in body]
    causes = ["", "Cause of death over %d games:" % config.N_TEST_GAMES, ""]
    causes += [f"- {name}: " + ", ".join(f"{c}={n}" for c, n in s["causes"].items() if n)
               for name, s in rows.items()]
    with open(os.path.join(config.RESULT_DIR, "results_table.md"), "w") as f:
        f.write("\n".join(lines + causes) + "\n")
    return "\n".join(lines + causes)


def _save_fig(name):
    os.makedirs(config.FIGURE_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(config.FIGURE_DIR, name), dpi=150)
    plt.close()


def chart_fitness(history):
    gens = [h["generation"] for h in history]
    plt.figure(figsize=(6, 4))
    plt.plot(gens, [h["best"] for h in history], marker="o", label="Best of generation")
    plt.plot(gens, [h["mean"] for h in history], marker="s", label="Population mean")
    plt.xlabel("Generation")
    plt.ylabel("Fitness (10 x score + 0.1 x steps)")
    plt.title("GA convergence: fitness per generation")
    plt.legend()
    plt.grid(alpha=0.3)
    _save_fig("fitness_per_generation.png")


def chart_bar(rows, key, std_key, ylabel, title, filename):
    names = list(rows)
    values = [rows[n][key] for n in names]
    errors = [rows[n][std_key] / np.sqrt(config.N_TEST_GAMES) for n in names]   # standard error
    plt.figure(figsize=(5, 4))
    plt.bar(names, values, yerr=errors, capsize=6, color=[COLOURS[n] for n in names])
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(axis="y", alpha=0.3)
    _save_fig(filename)


def chart_nodes(rows):
    names = ["BFS", "A*"]
    values = [rows[n]["avg_nodes_per_move"] for n in names]
    plt.figure(figsize=(5, 4))
    bars = plt.bar(names, values, color=[COLOURS[n] for n in names])
    plt.bar_label(bars, fmt="%.1f")
    plt.ylabel("Nodes expanded per move")
    plt.title("Why heuristics matter: search effort")
    plt.grid(axis="y", alpha=0.3)
    _save_fig("nodes_per_move.png")


def chart_causes(rows):
    names = list(rows)
    bottom = np.zeros(len(names))
    plt.figure(figsize=(5.5, 4))
    for cause in CAUSES:
        counts = np.array([rows[n]["causes"][cause] for n in names])
        if counts.sum() == 0:
            continue
        plt.bar(names, counts, bottom=bottom, label=cause)
        bottom += counts
    plt.ylabel("Games (out of %d)" % config.N_TEST_GAMES)
    plt.title("How the snakes died")
    plt.legend()
    _save_fig("death_causes.png")


def chart_distribution(all_results):
    names = list(all_results)
    plt.figure(figsize=(5, 4))
    plt.boxplot([[r.score for r in all_results[n]] for n in names], tick_labels=names)
    plt.ylabel("Score per game")
    plt.title("Score distribution over %d games" % config.N_TEST_GAMES)
    plt.grid(axis="y", alpha=0.3)
    _save_fig("score_distribution.png")


def main():
    print("Training the genetic algorithm (this takes a few minutes)...")
    weights, history = evolve()
    save_weights(weights)
    print("Evolved weights [safe, closer, space, exits]:", np.round(weights, 3))

    print(f"Evaluating on {config.N_TEST_GAMES} held-out games (seeds 0..{config.N_TEST_GAMES - 1})...")
    agents = [BFSAgent(), AStarAgent(), GAAgent(weights)]
    all_results = {agent.name: evaluate_agent(agent) for agent in agents}
    rows = {name: summarise(res) for name, res in all_results.items()}

    print(save_table(rows))
    chart_fitness(history)
    chart_bar(rows, "avg_score", "std_score", "Average score (food eaten)",
              "Average score (error bars: standard error)", "avg_score.png")
    chart_bar(rows, "avg_survival", "std_survival", "Average survival time (steps)",
              "Average survival time (error bars: standard error)", "survival_time.png")
    chart_nodes(rows)
    chart_causes(rows)
    chart_distribution(all_results)
    print("Charts saved in", config.FIGURE_DIR)


if __name__ == "__main__":
    main()
