import unittest

from config import QUANTITY_ESTATES
from domain.estate import Estate
from domain.player import PlayerFactory


class EstateTest(unittest.TestCase):
    """
    Cada propriedade tem:
    - um custo de venda,
    - um valor de aluguel,
    - um proprietário caso já estejam compradas,
    - e seguem uma determinada ordem no tabuleiro.
    """

    def setUp(self) -> None:
        self.sale_price_valid = 99.99
        self.rent_value_valid = 49.99
        self.owner_valid = PlayerFactory.create(_id=1)

    def test_constructor_with_input_values(self):
        sale_price = self.sale_price_valid
        rent_value = self.rent_value_valid
        owner = self.owner_valid

        estate = Estate(sale_price=sale_price, rent_value=rent_value, owner=owner)

        self.assertIsInstance(estate, Estate)
        self.assertEqual(estate.sale_price, self.sale_price_valid)
        self.assertEqual(estate.rent_value, self.rent_value_valid)
        self.assertEqual(estate.owner, self.owner_valid)

    def test_constructor_without_owner(self):
        sale_price = self.sale_price_valid
        rent_value = self.rent_value_valid

        estate = Estate(
            sale_price=sale_price,
            rent_value=rent_value,
        )

        self.assertIsNone(estate.owner)

    def test_factory_estates_with_quantity_20_default(self):
        estates = Estate.factory_estates()
        self.assertEqual(len(estates), QUANTITY_ESTATES)

    def test_factory_estates_with_given_quantity(self):
        estates = Estate.factory_estates(quantity=99)
        self.assertEqual(len(estates), 99)

    @unittest.skip
    def test_if_factory_estates_dont_repeat_values(self):
        """
        Cada propriedade tem UM custo de venda, UM valor de aluguel
        """
        pass

    @unittest.skip
    def test_if_order_is_correct(self):
        """
        Cada propriedade... e seguem uma determinada ordem no tabuleiro.
        """
        pass
