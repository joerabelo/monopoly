import abc
from dataclasses import dataclass
from typing import Any

from config import QUANTITY_ESTATES

from . import logger


@dataclass
class PlayerAbstract(abc.ABC):
    balance: float = 300.0  # TODO: change field name to: amount
    position: int = 0
    turns: int = 0
    id: int = 1

    @property
    def balance_negative(self) -> bool:
        return self.balance < 0

    def move_spaces(self, spaces: int) -> None:
        _new_position = self.position + spaces

        self.position = _new_position % QUANTITY_ESTATES
        logger.info(
            f"\tPlayer(id={self.id}) moved ({spaces}) spaces and new position is [{self.position}]"
        )

        full_turn = _new_position >= QUANTITY_ESTATES
        if full_turn:
            self.full_turn()

    def full_turn(self, bonus: float = 100.0) -> None:
        """
        Ao completar uma volta no tabuleiro, o jogador ganha 100 de saldo.
        """
        self.turns += 1
        self.balance += bonus
        logger.info(
            f"\tPlayer(id={self.id}) completed ({self.turns}) lap and +$100. New balance: {self.balance:+.2f}"
        )

    @abc.abstractmethod
    def validate_purchase_behavioral_rules(self, estate: Any) -> bool:
        raise NotImplementedError()
