import unittest
from dataclasses import is_dataclass
from random import randint

from domain.player import BehaviorEnum, PlayerFactory
from domain.player.__player_abstract import PlayerAbstract


class PlayerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.player = PlayerFactory.create()

    def test_constructor_with_default_values(self):
        pass

    def test_constructor_success(self):
        player = PlayerFactory.create()
        self.assertEqual(player.id, 1)
        self.assertEqual(player.behavior, BehaviorEnum.RANDOM)
        self.assertEqual(player.balance, 300.0)
        self.assertEqual(player.position, 0)
        self.assertEqual(player.turns, 0)

        player = PlayerFactory.create(behavior=BehaviorEnum.WARY, _id=2)
        self.assertEqual(player.id, 2)
        self.assertEqual(player.balance, 300.0)

        player = PlayerFactory.create(
            behavior=BehaviorEnum.PICKY, balance=123.456, _id=3
        )
        self.assertEqual(player.id, 3)
        self.assertEqual(player.behavior, BehaviorEnum.PICKY)
        self.assertEqual(player.balance, 123.456)

    @unittest.skip
    def test_constructor_failed(self):
        # TODO: Fazer falhar com dados invalidos
        amount_str = "fail"
        player = PlayerFactory.create(_id=1, balance=amount_str)
        self.assertEqual(player.balance, amount_str)

    @unittest.skip
    def test_constructor_dont_allow_equals_ids(self):
        _id = 1
        player1 = PlayerFactory.create(_id=_id)

        with self.assertRaises(ValueError) as context:
            player2 = PlayerFactory.create(_id=_id)

        self.assertIsNotNone(player1)
        self.assertEqual(player1.id, 1)
        self.assertIsNone(player2)

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(PlayerAbstract))

    def test_move_spaces(self):
        """
        ...que determina quantas espaços no tabuleiro o jogador vai andar.
        """
        spaces = randint(1, 6)
        player = self.player

        player.move_spaces(spaces=spaces)

        self.assertEqual(player.position, spaces)

    def test_move_spaces_between_0_and_19(self):
        """
        A posiçao deve estar entre 0 e 19 pois e o numero de propriedades/casas validas
        """
        spaces_wrong = 20
        player = self.player

        player.move_spaces(spaces=spaces_wrong)

        self.assertEqual(player.position, 0)
        self.assertGreaterEqual(player.position, 0)
        self.assertLess(player.position, 20)

    def test_if_player_received_100_if_full_turn(self):
        """
        Ao completar uma volta no tabuleiro, o jogador ganha 100 de saldo.
        """
        player = PlayerFactory.create(balance=300)

        player.full_turn()
        self.assertEqual(player.balance, 400)
        self.assertEqual(player.turns, 1)

        player.full_turn()
        self.assertEqual(player.balance, 500)
        self.assertEqual(player.turns, 2)

    @unittest.skip
    def test_if_player_loses_when_balance_is_negative(self):
        """
        Um jogador que fica com saldo negativo perde o jogo, e não joga mais.
        Perde suas propriedades e portanto podem ser compradas por qualquer outro jogador.
        """
        # player = PlayerAbstract.create_players(qtd_players=1, default_balance=100)
        pass
