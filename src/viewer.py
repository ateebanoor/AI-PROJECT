"""Optional Pygame window to watch an agent play. The AI never depends on this file."""
import config
from game import SnakeGame


def watch(agent, seed=0):
    """Show one game played by agent. Close the window or press ESC to stop."""
    try:
        import pygame
    except ImportError:
        raise RuntimeError("Pygame is not installed. Run: pip install -r requirements.txt") from None

    size = config.GRID_SIZE * config.CELL_PIXELS
    pygame.init()
    screen = pygame.display.set_mode((size, size + 30))
    pygame.display.set_caption(f"Snake - {agent.name}")
    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    def cell_rect(cell):
        return pygame.Rect(cell[0] * config.CELL_PIXELS, cell[1] * config.CELL_PIXELS,
                           config.CELL_PIXELS - 2, config.CELL_PIXELS - 2)

    game = SnakeGame(seed=seed)
    agent.reset()
    running = True
    while running and game.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                             and event.key == pygame.K_ESCAPE):
                running = False
        game.step(agent.choose_move(game))

        screen.fill((20, 20, 20))
        if game.food:
            pygame.draw.rect(screen, (220, 60, 60), cell_rect(game.food))
        for cell in game.snake.cells:
            pygame.draw.rect(screen, (80, 200, 120), cell_rect(cell))
        pygame.draw.rect(screen, (30, 140, 70), cell_rect(game.snake.head))
        text = f"{agent.name}   score {game.score}   steps {game.steps}"
        screen.blit(font.render(text, True, (255, 255, 255)), (8, size + 6))
        pygame.display.flip()
        clock.tick(config.FPS)

    if running:                     # game over: show the result for a moment
        print(f"Game over ({game.death_cause}): score {game.score}, steps {game.steps}")
        pygame.time.wait(1500)
    pygame.quit()
