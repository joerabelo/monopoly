import unittest
from unittest.mock import Mock, patch

from domain.board import Board
from domain.estate import Estate
from domain.player import BehaviorEnum, PlayerFactory


class BoardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board.create()

    def test_constructor(self):
        """
        Nesse jogo, o tabuleiro é composto por 20 propriedades em sequência.
        ...idealizamos uma partida com 4 diferentes tipos de possíveis jogadores
        """
        board = Board(players=[PlayerFactory.create()])
        self.assertEqual(len(board.players), 1)
        self.assertEqual(len(board.estates), 20)

    # def test_start_match(self):
    #     """
    #     Os jogadores sempre começam uma partida com saldo de 300 para cada um.
    #     """
    #     self.board.start_match()
    #
    #     for p in self.board.player:
    #         self.assertEqual(p.balance, 300.0)
    #
    def test_create(self):
        """
        Nesse jogo, o tabuleiro é composto por 20 propriedades em sequência.
        ...idealizamos uma partida com 4 diferentes tipos de possíveis jogadores
        Os jogadores sempre começam uma partida com saldo de 300 para cada um.
        """
        self.board.create()

        self.assertEqual(len(self.board.estates), 20)
        self.assertEqual(len(self.board.players), 4)
        for p in self.board.players:
            self.assertEqual(p.balance, 300.0)

    def test_roll_dice(self):
        """
        No começo da sua vez, o jogador joga um dado equiprovável de 6 faces
        """
        sided_number = Board.roll_dice()
        self.assertIn(sided_number, range(1, 7))

    def test_estate_purchase(self):
        """
        Ao cair em uma propriedade sem proprietário, o jogador pode escolher entre comprar ou não a propriedade.
        Esse é a única forma pela qual uma propriedade pode ser comprada.

        Ao comprar uma propriedade, o jogador perde o dinheiro e ganha a posse da propriedade.
        """
        sale_price = 49.99
        balance_before_purchase = 200.0
        balance_after_purchase = balance_before_purchase - sale_price
        buyer = PlayerFactory.create(
            _id=1,
            balance=balance_before_purchase,
            behavior=BehaviorEnum.IMPULSIVE,
        )
        estate = Estate(
            sale_price=sale_price,
            rent_value=22,
        )

        sold = self.board.purchase(player=buyer, estate=estate)

        self.assertTrue(sold)
        self.assertEqual(estate.owner, buyer)
        self.assertEqual(buyer.balance, balance_after_purchase)

    def test_estate_purchase_only_if_player_balance_equal_or_greater_sale_price(self):
        """
        Jogadores só podem comprar propriedades caso ela não tenha dono e o jogador tenha o dinheiro da venda
        """
        sale_price = 49.99
        balance_before = 49.98
        buyer = PlayerFactory.create(_id=1, balance=balance_before)
        estate = Estate(
            sale_price=sale_price,
            rent_value=22,
        )

        sold = self.board.purchase(player=buyer, estate=estate)

        self.assertFalse(sold)
        self.assertIsNone(estate.owner)
        self.assertEqual(buyer.balance, balance_before)

    def test_estate_already_has_owner_not_allow_purchase(self):
        """
        Ao cair em uma propriedade sem proprietário, o jogador pode escolher entre comprar ou não a propriedade.
        """
        sale_price = 49.99
        balance = 200.0
        buyer = PlayerFactory.create(_id=1, balance=balance)
        owner = PlayerFactory.create(_id=2, balance=100.0)
        estate = Estate(sale_price=sale_price, rent_value=22, owner=owner)

        sold = self.board.purchase(player=buyer, estate=estate)

        self.assertFalse(sold)
        self.assertEqual(buyer.balance, balance)
        self.assertEqual(estate.owner, owner)
        self.assertIsNotNone(
            estate.owner
        )  # TODO: Maybe redundant with: assertEqual(estate.owner, owner)
        self.assertNotEqual(
            estate.owner, buyer
        )  # TODO: Maybe redundant with: assertEqual(estate.owner, owner)

    def test_pay_rent(self):
        """
        Ao cair em uma propriedade que tem proprietário,
        ele deve pagar ao proprietário o valor do aluguel da propriedade.
        """
        rent_value = 99.99

        tenant_balance_before = 200.0
        tenant_balance_after = tenant_balance_before - rent_value

        owner_balance_before = 150.0
        owner_balance_after = owner_balance_before + rent_value

        owner = PlayerFactory.create(_id=1, balance=owner_balance_before)
        tenant = PlayerFactory.create(_id=2, balance=tenant_balance_before)
        estate = Estate(
            owner=owner,
            sale_price=10,
            rent_value=rent_value,
        )

        paid = self.board.pay_rent(player=tenant, estate=estate)

        self.assertTrue(paid)
        self.assertNotEqual(estate.owner, tenant)
        self.assertEqual(tenant.balance, tenant_balance_after)
        self.assertEqual(estate.owner.balance, owner_balance_after)

    def test_player_is_not_allowed_to_pay_his_own_rent(self):
        rent_value = 100.0

        balance_before = 200.0
        balance_after = balance_before - rent_value  # $100

        owner = tenant = PlayerFactory.create(_id=1, balance=balance_before)
        estate = Estate(
            owner=owner,
            sale_price=10,
            rent_value=rent_value,
        )

        paid = self.board.pay_rent(player=tenant, estate=estate)

        self.assertFalse(paid)
        self.assertEqual(estate.owner, owner)
        self.assertEqual(estate.owner, tenant)
        self.assertEqual(tenant.balance, balance_before)
        self.assertEqual(estate.owner.balance, balance_before)
        self.assertNotEqual(tenant.balance, balance_after)
        self.assertNotEqual(estate.owner.balance, balance_after)

    @unittest.skip
    def test_if_game_has_four_players(self):
        """
        ...idealizamos uma partida com 4 diferentes tipos de possíveis jogadores
        """
        pass

    @unittest.skip
    def test_if_game_has_a_player_of_each_behavior(self):
        """
        O jogador um é impulsivo;
        O jogador dois é exigente;
        O jogador três é cauteloso;
        O jogador quatro é aleatório;
        """
        pass

    def test_purchase_player_impulsive(self):
        """
        O jogador impulsivo compra qualquer propriedade sobre a qual ele parar.
        """
        behavior = BehaviorEnum.IMPULSIVE
        sale_price = 49.99
        balance_before_purchase = 200.0
        balance_after_purchase = balance_before_purchase - sale_price
        buyer = PlayerFactory.create(
            _id=1,
            balance=balance_before_purchase,
            behavior=behavior,
        )
        estate = Estate(
            sale_price=sale_price,
            rent_value=22,
        )

        sold = self.board.purchase(player=buyer, estate=estate)

        self.assertTrue(sold)
        self.assertEqual(estate.owner, buyer)
        self.assertEqual(buyer.balance, balance_after_purchase)

    def test_purchase_player_picky__rent_greater_50(self):
        """
        O jogador exigente compra qualquer propriedade, desde que o valor do aluguel dela seja maior do que 50.
        """
        behavior = BehaviorEnum.PICKY
        rent_value = 50.01
        sale_price = 99.99
        balance_before_purchase = 300.0
        balance_after_purchase = balance_before_purchase - sale_price
        buyer = PlayerFactory.create(
            _id=1,
            balance=balance_before_purchase,
            behavior=behavior,
        )
        estate = Estate(
            sale_price=sale_price,
            rent_value=rent_value,
        )

        sold = self.board.purchase(player=buyer, estate=estate)

        self.assertTrue(sold)
        self.assertEqual(estate.owner, buyer)
        self.assertEqual(buyer.balance, balance_after_purchase)

    def test_purchase_player_picky__dont_allow_if_rent_less_or_equal_50(self):
        """
        O jogador exigente compra qualquer propriedade, desde que o valor do aluguel dela seja maior do que 50.
        """
        behavior = BehaviorEnum.PICKY
        rent_value = 50.0
        sale_price = 99.99
        balance_before_purchase = 300.0
        buyer = PlayerFactory.create(
            _id=1,
            balance=balance_before_purchase,
            behavior=behavior,
        )
        estate = Estate(
            sale_price=sale_price,
            rent_value=rent_value,
        )

        sold = self.board.purchase(player=buyer, estate=estate)

        self.assertFalse(sold)
        self.assertIsNone(estate.owner)
        self.assertEqual(buyer.balance, balance_before_purchase)

    def test_purchase_player_wary__with_80_left_over(self):
        """
        O jogador cauteloso compra qualquer propriedade desde que
        ele tenha uma reserva de 80 saldo sobrando depois de realizada a compra.
        """
        behavior = BehaviorEnum.WARY
        sale_price = 100.0
        balance_before_purchase = 180.0
        balance_after_purchase = balance_before_purchase - sale_price
        buyer = PlayerFactory.create(
            _id=1,
            balance=balance_before_purchase,
            behavior=behavior,
        )
        estate = Estate(
            sale_price=sale_price,
            rent_value=49.98,
        )

        sold = self.board.purchase(player=buyer, estate=estate)

        self.assertTrue(sold)
        self.assertEqual(estate.owner, buyer)
        self.assertEqual(buyer.balance, balance_after_purchase)
        self.assertEqual(buyer.balance, 80.0)

    def test_purchase_player_wary__dont_allow_if_there_is_not_80_left(self):
        """
        O jogador cauteloso compra qualquer propriedade desde que
        ele tenha uma reserva de 80 saldo sobrando depois de realizada a compra.
        """
        behavior = BehaviorEnum.WARY
        sale_price = 100.0
        balance_before_purchase = 179.99
        buyer = PlayerFactory.create(
            _id=1,
            balance=balance_before_purchase,
            behavior=behavior,
        )
        estate = Estate(
            sale_price=sale_price,
            rent_value=49.98,
        )

        sold = self.board.purchase(player=buyer, estate=estate)

        self.assertFalse(sold)
        self.assertIsNone(estate.owner)
        self.assertEqual(buyer.balance, balance_before_purchase)
        self.assertEqual(buyer.balance, 179.99)

    def test_purchase_player_random__return_positive(self):
        """
        O jogador aleatório compra a propriedade que ele parar em cima com probabilidade de 50%.
        """
        behavior = BehaviorEnum.RANDOM
        sale_price = 100.0
        balance_before_purchase = 300.0
        balance_after_purchase = balance_before_purchase - sale_price
        buyer = PlayerFactory.create(
            _id=1,
            balance=balance_before_purchase,
            behavior=behavior,
        )
        estate = Estate(
            sale_price=sale_price,
            rent_value=49.98,
        )

        with patch(
            "domain.player.player_random.PlayerRandom.validate_purchase_behavioral_rules",
            Mock(return_value=True),
        ):
            sold = self.board.purchase(player=buyer, estate=estate)

        self.assertTrue(sold)
        self.assertEqual(estate.owner, buyer)
        self.assertEqual(buyer.balance, balance_after_purchase)
        self.assertEqual(buyer.balance, 200.0)

    def test_purchase_player_random__return_negative(self):
        """
        O jogador aleatório compra a propriedade que ele parar em cima com probabilidade de 50%.
        """
        behavior = BehaviorEnum.RANDOM
        sale_price = 100.0
        balance_before_purchase = 300.0
        balance_after_purchase = balance_before_purchase - sale_price
        buyer = PlayerFactory.create(
            _id=1,
            balance=balance_before_purchase,
            behavior=behavior,
        )
        estate = Estate(
            sale_price=sale_price,
            rent_value=49.98,
        )

        with patch(
            "domain.player.player_random.PlayerRandom.validate_purchase_behavioral_rules",
            Mock(return_value=False),
        ):
            sold = self.board.purchase(player=buyer, estate=estate)

        self.assertFalse(sold)
        self.assertIsNone(estate.owner)
        self.assertEqual(buyer.balance, balance_before_purchase)
        self.assertEqual(buyer.balance, 300.0)

    @unittest.skip
    def test_player_lost(self):
        """
        Um jogador que fica com saldo negativo perde o jogo, e não joga mais.
        Perde suas propriedades e portanto podem ser compradas por qualquer outro jogador.
        """
        pass

    def test_take_one_estate_loser_player(self):
        """
        Um jogador que... perde o jogo... Perde suas propriedades...
        """
        player = self.board.players[0]
        estate = self.board.estates[0]
        self.board.purchase(player=player, estate=estate)

        self.board.take_estates(player=player)

        self.assertIsNone(estate.owner)

    def test_take_various_estates_loser_player(self):
        """
        Um jogador que... perde o jogo... Perde suas propriedades...
        """
        player = self.board.players[0]
        estate1 = self.board.estates[0]
        estate2 = self.board.estates[1]
        estate3 = self.board.estates[2]
        self.board.purchase(player=player, estate=estate1)
        self.board.purchase(player=player, estate=estate2)
        self.board.purchase(player=player, estate=estate3)

        self.board.take_estates(player=player)

        self.assertIsNone(estate1.owner)
        self.assertIsNone(estate2.owner)
        self.assertIsNone(estate3.owner)

        # game = Board.create_game()
        # game.start_match()
        # game.play()
        #
        #
        # player1 = PlayerFactory.create(_id=1, balance=15.99)
        # estate1 = Estate(
        #     owner=player1,
        #     sale_price=50,
        #     rent_value=16.01,
        # )
        #
        # player2 = PlayerFactory.create(_id=2)
        # estate2 = Estate(
        #     owner=player2,
        #     sale_price=50,
        #     rent_value=16.01,
        # )
        # paid = estate2.pay_rent(tenant=player1)
        #
        # estate2.player_lost(loser=player1)
        #
        # self.assertTrue(paid)
        # self.assertIsNone(estate1.owner)
        # self.assertNotIn(player1, )
