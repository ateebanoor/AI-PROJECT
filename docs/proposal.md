---
title: "Project Proposal: Snake AI, BFS vs A* vs Genetic Algorithm"
---

**AL-2002 Artificial Intelligence (Lab), Fall 2026, FAST-NUCES Karachi**

| | |
|---|---|
| Group members | *[Member 1 name, roll no.]*, *[Member 2 name, roll no.]* |
| Group leader | *[name]* |
| Section / idea number | *[section]* / *[idea number from the group sheet]* |

## 1. Problem and motivation

The classic game of Snake is a small but honest planning problem. The snake must reach food while its own body keeps growing into an obstacle. A snake that always takes the shortest path to the food looks clever, but sooner or later it wraps itself into a dead end. We want to show, with measurements, three things:

1. why a **heuristic** matters (A* against BFS on the same problem),
2. how a snake that **only chases food** traps itself, and
3. how **evolution** can discover a safer way to choose moves.

Three snakes will play: a BFS snake, an A* snake, and a snake that follows a simple weighted decision rule whose weights are evolved by a genetic algorithm. They will be compared on score and survival time.

## 2. Problem formulation

**State.** Board size (10x10), the snake's cells in order from head to tail, the food cell, the score and the number of moves since the last food.

**Actions.** UP, DOWN, LEFT, RIGHT.

**Transition.** The head moves one cell. If it lands on the food the snake grows by one and new food appears on a random free cell; otherwise the tail follows.

**Terminal conditions.** The head leaves the board, hits the body, or 100 moves pass without eating (this stops endless loops).

**Goal and cost for the search agents.** Reach the food cell; every move costs 1.

### PEAS description

| | |
|---|---|
| **Performance measure** | Score (food eaten) and survival time (moves made before dying). |
| **Environment** | A 10x10 grid with walls, the snake's body and one piece of food. |
| **Actuators** | Choose one of four moves each turn. |
| **Sensors** | The full board: head, body and food positions. |

### Environment classification

Fully observable; deterministic movement (only the position of new food is random, and it is seeded); static (the game waits for the agent); discrete; single-agent; sequential.

### Agent types

BFS and A* snakes are **goal-based agents**: they plan a path to a goal. The GA snake is a **utility-based agent**: it scores each possible move with a weighted utility and takes the best one.

## 3. Planned design (OOP)

At least five classes: `Snake` (the body, encapsulated), `SnakeGame` (the environment and rules), `Agent` (base class), `PathAgent(Agent)` with subclasses `BFSAgent` and `AStarAgent` that **override** `find_path`, and `GAAgent(Agent)` that overrides `choose_move`. All randomness uses a seeded `random.Random`, so every experiment can be reproduced.

## 4. AI techniques

| Lab | Technique | How it is used |
|---|---|---|
| 04 | Uninformed search | BFS written from scratch: FIFO frontier, explored set, node counts, path and cost. |
| 05 | Informed search | A* written from scratch with the Manhattan-distance heuristic; admissibility argued; node count compared with BFS. |
| 06 | Local search / genetic algorithm | Evolves 4 weights of a move-scoring rule. Fitness = 10 x score + 0.1 x steps, averaged over 5 training games. Population 20, 30 generations, tournament selection, uniform crossover, Gaussian mutation, 2 elites. Fitness per generation is plotted. |

The GA rule scores a move from four features: is it safe, does it get closer to the food, how much of the board is still reachable (flood fill), and how many exits the new cell has.

**Write-it-yourself rule.** BFS, A* and the GA are our own code. No search library is used. Only NumPy (arrays), Matplotlib (charts) and Pygame (optional window) are needed. No deep-learning framework, paid API or deployment.

## 5. Data and environment

No dataset is needed. Games are generated from integer seeds. Pygame provides an optional window to watch a snake; the experiments run without it.

## 6. Evaluation plan

- Each snake plays **100 games on the same seeds** (0 to 99); the GA is trained on different seeds (1000 to 1004) so that its evaluation is on unseen games.
- **Metrics:** average score, average survival time (with standard deviation), maximum score, cause of death, and nodes expanded per move for BFS and A*.
- **Outputs:** one results table and at least three labelled charts: fitness per generation, average score and survival time, and nodes per move.
- **Baselines:** BFS is the baseline for A*; both search snakes are the baseline for the GA snake.
- **Expected outcome (a hypothesis, not a result):** BFS and A* find paths of equal length but A* expands far fewer nodes; both trap themselves; the GA snake survives longer.

## 7. Scope check

Three agents and one 10x10 environment is the right size for two students over the remaining weeks: the game and search code are short, and the GA only has four parameters to evolve. If one member works alone, the GA snake is the part to simplify (smaller population, fewer generations).

## 8. Work division

| Member | Responsibility |
|---|---|
| *[Member 1]* | Game environment (`game.py`), BFS and A* (`search.py`), path agents, unit tests. |
| *[Member 2]* | GA (`ga.py`), GA agent and features (`agents.py`), experiment script and charts, Pygame viewer. |
| Both | README, proposal, report, repository set-up, rehearsal for the viva. |

Each member commits from their own GitHub account.

## 9. Milestones

| When | Milestone |
|---|---|
| Week 10 | Proposal approved; repository created; game environment working. |
| Week 11 | BFS and A* snakes working and tested. |
| Week 12 | GA snake working; training runs. |
| Week 13 | Experiment script, table and charts. |
| Week 14 | Report written; test from a fresh clone on another machine. |
| Week 15 | Submit repository link on Google Classroom; individual viva. |

## 10. Risks

| Risk | Plan |
|---|---|
| Training the GA takes too long | Keep the board small (10x10) and only evolve four weights. |
| A* shows no advantage in score | That is expected: both find shortest paths. The advantage to measure is search effort. |
| Results change between runs | Seed every random source. |
