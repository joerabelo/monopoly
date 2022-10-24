from typing import Any

from domain.player import BehaviorEnum, PlayerAbstract


class PlayerPicky(PlayerAbstract):
    behavior = BehaviorEnum.PICKY

    def validate_purchase_behavioral_rules(self, estate: Any) -> bool:
        """
        O jogador exigente compra qualquer propriedade, desde que o valor do aluguel dela seja maior do que 50.
        """
        return estate.rent_value > 50.0
