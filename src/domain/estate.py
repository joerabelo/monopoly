import random
from dataclasses import dataclass

import log
from config import LOG_LEVEL, QUANTITY_ESTATES
from domain.player.__player_abstract import PlayerAbstract

logger = log.init_logger(__name__, LOG_LEVEL)


@dataclass()
class Estate:
    sale_price: float
    rent_value: float
    owner: PlayerAbstract = None

    @property
    def has_no_owner(self) -> bool:
        return self.owner is None

    @staticmethod
    def factory_estates(quantity: int = QUANTITY_ESTATES) -> list:
        return [
            Estate(
                sale_price=random.uniform(100, 150),  # noqa
                rent_value=random.uniform(10, 60),  # noqa
            )
            for i in range(0, quantity)
        ]

    def add_owner(self, buyer: PlayerAbstract) -> bool:
        if self.owner is not None:
            self.owner = buyer
            return True
        return False
