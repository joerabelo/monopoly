import log
from config import LOG_LEVEL
from domain.player import BehaviorEnum
from domain.player.player_impulsive import PlayerImpulsive
from domain.player.player_picky import PlayerPicky
from domain.player.player_random import PlayerRandom
from domain.player.player_wary import PlayerWary

logger = log.init_logger(__name__, LOG_LEVEL)


class PlayerFactory:
    @staticmethod
    def create(
        behavior: BehaviorEnum = BehaviorEnum.RANDOM,
        balance: float = 300.0,
        _id: int = 1,
    ):
        player = None

        if behavior == BehaviorEnum.IMPULSIVE:
            player = PlayerImpulsive(balance=balance, id=_id)
        elif behavior == BehaviorEnum.PICKY:
            player = PlayerPicky(balance=balance, id=_id)
        elif behavior == BehaviorEnum.WARY:
            player = PlayerWary(balance=balance, id=_id)
        elif behavior == BehaviorEnum.RANDOM:
            player = PlayerRandom(balance=balance, id=_id)

        logger.debug(f"Created player: {player}")
        return player
