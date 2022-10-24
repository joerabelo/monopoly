from random import randint
from typing import Any

from domain.player import BehaviorEnum, PlayerAbstract


class PlayerRandom(PlayerAbstract):
    behavior = BehaviorEnum.RANDOM

    def validate_purchase_behavioral_rules(self, estate: Any) -> bool:
        """
        O jogador aleatório compra a propriedade que ele parar em cima com probabilidade de 50%.
        """
        return bool(randint(0, 1))  # noqa S311
