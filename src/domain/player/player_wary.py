from typing import Any

from domain.player import BehaviorEnum, PlayerAbstract


class PlayerWary(PlayerAbstract):
    behavior = BehaviorEnum.WARY

    def validate_purchase_behavioral_rules(self, estate: Any) -> bool:
        """
        O jogador cauteloso compra qualquer propriedade desde que ele tenha
        uma reserva de 80 saldo sobrando depois de realizada a compra.
        """
        return (self.balance - estate.sale_price) >= 80.0
