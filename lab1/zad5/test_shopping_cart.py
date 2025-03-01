import unittest
from shopping_cart import ShoppingCart

class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_items(self):
        self.cart.add_item("Apple",1.5,2)
        self.assertIn("Apple",self.cart.items)
        self.assertEqual(self.cart.items["Apple"]["quantity"],2)
        self.assertEqual(self.cart.items["Apple"]["price"],1.5)

    def test_add_multiple_items(self):
        self.cart.add_item("Apple",1.5,2)
        self.cart.add_item("Banana",2.5,4)
        self.assertEqual(len(self.cart.items),2)
        self.assertEqual(self.cart.items["Apple"]["quantity"],2)
        self.assertEqual(self.cart.items["Banana"]["price"],2.5)

    def test_remove_item(self):
            self.cart.add_item("Apple",1.5,2)
            self.cart.remove_item("Apple")
            self.assertNotIn("Apple",self.cart.items)

    def test_remove_no_existing_item(self):

        with self.assertRaises(ValueError):
            self.cart.remove_item("Apple")

    def test_get_total(self):
        self.cart.add_item("Apple",1.5,4)
        self.cart.add_item("Banana",2.5,12)
        self.assertEqual(self.cart.get_total(), 36)

    def test_get_total_from_clear_cart(self):
        self.assertEqual(self.cart.get_total(), 0)

    def test_clear_cart(self):
        self.cart.add_item("Apple",1.5,2)
        self.cart.add_item("Banana",2.5,12)
        self.cart.clear()
        self.assertEqual(self.cart.get_total(), 0)

    if __name__ == '__main__':
        unittest.main()

