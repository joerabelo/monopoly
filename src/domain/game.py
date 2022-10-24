import log
from config import LOG_LEVEL, NUMBER_OF_RUNS
from domain.board import Board

logger = log.init_logger("main.py", LOG_LEVEL)


class Game:
    results: list

    def __init__(self):
        self.results = list()

    def play(self, number_of_runs: int = NUMBER_OF_RUNS):
        for i in range(0, number_of_runs):
            logger.warning(f"*** Started the Game ({i}) ***")

            board = Board.create()
            result = board.match()
            self.results.append(result)

            self.__log_resume(board, i)

    @staticmethod
    def __log_resume(board, i):
        logger.warning(f"==== Result of Game ({i}) with {board.rounds} rounds ====")
        players = sorted(board.players + board.losers, key=lambda player: player.id)
        for p in players:
            logger.warning(
                f"Player(id={p.id}, rounds={p.turns:4d}, balance={p.balance:+10.2f}, behavior={p.behavior})"
            )
        logger.warning(f"*** End the Game ({i}) ***\n")
