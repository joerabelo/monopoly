from dataclasses import dataclass, field
from random import randint
from typing import List

import log
from config import LOG_LEVEL
from domain.estate import Estate
from domain.player import BehaviorEnum, PlayerFactory
from domain.player.__player_abstract import PlayerAbstract

logger = log.init_logger(__name__, LOG_LEVEL)


@dataclass()
class Board:
    players: List[PlayerAbstract]  # = field(default_factory=players_factory)
    losers: List[PlayerAbstract] = field(default_factory=lambda: list())
    """
    Nesse jogo, o tabuleiro é composto por 20 propriedades em sequência.
    """
    estates: List[Estate] = field(default_factory=Estate.factory_estates)
    rounds: int = 0
    winner: PlayerAbstract = None

    @property
    def qtd_players(self):
        return len(self.players)

    def __post_init__(self):
        logger.debug("Created Board")
        logger.debug(f"Created Board with ({len(self.estates)}) estates")

    @staticmethod
    def create():
        """
        Os jogadores sempre começam uma partida com saldo de 300 para cada um.

        Cada um dos jogadores tem uma implementação de comportamento diferente,
        que dita as ações que eles vão tomar ao longo do jogo
        """
        players = [
            PlayerFactory.create(_id=1, behavior=BehaviorEnum.IMPULSIVE),
            PlayerFactory.create(_id=2, behavior=BehaviorEnum.PICKY),
            PlayerFactory.create(_id=3, behavior=BehaviorEnum.WARY),
            PlayerFactory.create(_id=4, behavior=BehaviorEnum.RANDOM),
        ]
        [logger.info(p) for p in players]
        board = Board(
            players=players,
        )
        logger.info("Created Board")
        return board

    def match(self):
        logger.warning("*** Match started ***")

        while not self.has_winner():

            for player in self.players:
                player.move_spaces(spaces=self.roll_dice())

                current_estate = self.estates[player.position]
                if current_estate.has_no_owner:
                    self.purchase(player=player, estate=current_estate)
                else:
                    self.pay_rent(player=player, estate=current_estate)

                if player.balance_negative:
                    self.take_estates(player=player)
                    self.remove_player(player=player)

        logger.warning("*** End of match ***")

        return {
            "timeout": int(self.rounds >= 1000),
            "rounds": self.rounds,
            "winner": self.winner,
            "behavior": {
                BehaviorEnum.IMPULSIVE.value: int(
                    self.winner.behavior == BehaviorEnum.IMPULSIVE
                ),
                BehaviorEnum.PICKY.value: int(
                    self.winner.behavior == BehaviorEnum.PICKY
                ),
                BehaviorEnum.WARY.value: int(self.winner.behavior == BehaviorEnum.WARY),
                BehaviorEnum.RANDOM.value: int(
                    self.winner.behavior == BehaviorEnum.RANDOM
                ),
            },
        }

    def take_estates(self, player: PlayerAbstract) -> None:
        """
        Perde suas propriedades (e portanto podem ser compradas por qualquer outro jogador)
        """
        for __estate in self.estates:
            if __estate.owner == player:
                __estate.owner = None
                logger.info(
                    f"\tEstate {__estate} has owner Player(id={player.id}) removed"
                )

    def remove_player(self, player: PlayerAbstract) -> None:
        """jogador que perde ... não joga mais"""
        self.losers.append(player)
        self.players.remove(player)
        logger.info(f"\tPlayer(id={player.id}) has removed from board")

    @staticmethod
    def roll_dice() -> int:
        """
        o jogador joga um dado equiprovável de 6 faces que determina quantas espaços no tabuleiro o jogador vai andar.
        """
        sided_number = randint(1, 6)  # noqa S311
        logger.debug(f"Roll dice sided number: {sided_number}")
        return sided_number

    @staticmethod
    def validate_purchase_general_rules(player: PlayerAbstract, estate: Estate) -> bool:
        """
        Jogadores só podem comprar propriedades caso ela não tenha dono e o jogador tenha o dinheiro da venda
        """
        return estate.owner is None and player.balance >= estate.sale_price

    def _is_valid_purchase(self, player: PlayerAbstract, estate: Estate) -> bool:
        return self.validate_purchase_general_rules(
            player=player, estate=estate
        ) and player.validate_purchase_behavioral_rules(estate=estate)

    def purchase(self, player: PlayerAbstract, estate: Estate) -> bool:
        valid = self._is_valid_purchase(player, estate)
        if valid:
            estate.owner = player
            player.balance -= estate.sale_price
            logger.info(
                f"\tPlayer(id={player.id}) purchase Estate({estate.sale_price:.2f}, {estate.rent_value:.2f}). New Balance = {player.balance:+.2f}"
            )
        else:
            logger.info(
                f"\tPlayer(id={player.id}) did not buy. Balance = {player.balance:+.2f}"
            )
        return valid

    def pay_rent(self, player: PlayerAbstract, estate: Estate) -> bool:
        if player.id is estate.owner.id:
            logger.info(
                f"\tPlayer(id={player.id}) already owner this estate. Balance = {player.balance:+.2f}"
            )
            return False

        player.balance -= estate.rent_value
        estate.owner.balance += estate.rent_value
        logger.info(
            f"\tTenant(id={player.id}) paid {estate.rent_value:.2f} rent to Owner(id={estate.owner.id}). New Balance = {player.balance:+.2f}"
        )

        return True

    def has_winner(self) -> bool:
        """
        ...quando restar somente um jogador com saldo positivo
        ...ou o jogo termina na milésima rodada
        """
        winner = None
        if not self.having_more_than_one_player() or not self.no_round_limit():
            winner = self.get_winner()
        return bool(winner)

    def having_more_than_one_player(self) -> bool:
        """
        Termina quando restar somente um jogador com saldo positivo, a qualquer momento da partida.
        Esse jogador é declarado o vencedor.
        TODO: create test this method
        """
        # has_winner = len(self.losers) == (len(self.players) - 1)
        has_winner = len(self.players) == 1
        return not has_winner

    def no_round_limit(self, limit_rounds: int = 1000) -> bool:
        """
        Caso o jogo demore muito...o jogo termina na milésima rodada
        """
        self.rounds += 1
        arrived = self.rounds == limit_rounds
        logger.info(f"Round: {self.rounds}")
        if arrived:
            logger.warning(f"The game has reached the limit of rounds ({limit_rounds})")
        return not arrived

    def get_winner(self) -> PlayerAbstract:
        """
        ...o jogo termina ... com a vitória do jogador com mais saldo.
        O critério de desempate é a ordem de turno dos jogadores nesta partida.
        """
        self.winner = sorted(
            (p for p in self.players if p not in self.losers),
            key=lambda p: (p.balance, p.turns),
        ).pop()
        # logger.warning(f'\n\n***** THE WINNER IS: {self.winner} ***** \n')
        logger.warning(f"*** THE WINNER IS: {self.winner} ***")
        return self.winner
