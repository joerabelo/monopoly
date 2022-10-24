from typing import Any

from domain.player import BehaviorEnum, PlayerAbstract


class PlayerImpulsive(PlayerAbstract):
    behavior = BehaviorEnum.IMPULSIVE

    def validate_purchase_behavioral_rules(self, estate: Any) -> bool:
        """
        O jogador impulsivo compra qualquer propriedade sobre a qual ele parar.
        """
        return True
