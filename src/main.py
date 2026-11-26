"""Console menu for the Snake AI project.   Run from the repository root:  python src/main.py"""
import config
from agents import AStarAgent, BFSAgent, GAAgent
from ga import evolve, load_weights, save_weights
from runner import play_game

MENU = """
=== Snake AI: BFS vs A* vs Genetic Algorithm ===
1) Watch the BFS snake
2) Watch the A* snake
3) Watch the GA snake
4) Train the GA snake (a few minutes)
5) Play one game of each snake in the console (no window)
6) Run the full experiment (see: python src/experiment.py)
0) Quit
"""


def make_agent(choice):
    """Build the agent for menu option 1, 2 or 3."""
    if choice == "1":
        return BFSAgent()
    if choice == "2":
        return AStarAgent()
    return GAAgent(load_weights())          # may raise FileNotFoundError / ValueError


def watch_agent(choice):
    from viewer import watch                # imported here so Pygame is optional
    watch(make_agent(choice))


def train():
    weights, _ = evolve()
    save_weights(weights)
    print("Saved weights:", [round(float(w), 3) for w in weights])


def quick_compare():
    for choice in ("1", "2", "3"):
        agent = make_agent(choice)
        result = play_game(agent, seed=0)
        print(f"{agent.name:3s}: score {result.score:2d}, steps {result.steps:3d}, died by {result.cause}")


def run_experiment():
    import experiment
    experiment.main()


def main():
    actions = {"1": lambda: watch_agent("1"), "2": lambda: watch_agent("2"),
               "3": lambda: watch_agent("3"), "4": train,
               "5": quick_compare, "6": run_experiment}
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            break
        if choice not in actions:
            print("Please type a number from 0 to 6.")
            continue
        try:
            actions[choice]()
        except (FileNotFoundError, ValueError, RuntimeError) as err:
            print("Cannot do that:", err)


if __name__ == "__main__":
    main()
