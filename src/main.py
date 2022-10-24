import log
from config import LOG_LEVEL
from domain.game import Game
from view import display_stdout

logger = log.init_logger("main.py", LOG_LEVEL)

if __name__ == "__main__":
    logger.warning("Application started\n")

    game = Game()
    game.play()

    display_stdout(game.results)
