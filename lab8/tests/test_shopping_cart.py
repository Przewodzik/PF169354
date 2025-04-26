import pytest

from lab8.src.shopping_cart import ShoppingCart,Product

@pytest.fixture
def sample_product1():
    return Product(1,"Tea",14.5)

@pytest.fixture
def sample_product2():
    return Product(2, "Coffee", 23)

@pytest.fixture
def empty_shopping_cart():
    return ShoppingCart()


@pytest.fixture
def filled_cart(empty_shopping_cart, sample_product1, sample_product2):

    empty_shopping_cart.add_product(sample_product1, 2)
    empty_shopping_cart.add_product(sample_product2, 5)
    return empty_shopping_cart

def test_adding_product(empty_shopping_cart, sample_product1, sample_product2):

    assert empty_shopping_cart.get_product_count() == 0
    empty_shopping_cart.add_product(sample_product1, 1)
    assert empty_shopping_cart.get_product_count() == 1
    assert empty_shopping_cart.get_total_price() == 14.5
    assert sample_product1.id in empty_shopping_cart.products.keys()

    with pytest.raises(ValueError):
        empty_shopping_cart.add_product(sample_product2, -2)

def test_adding_negative_quantity(empty_shopping_cart, sample_product2):

    with pytest.raises(ValueError):
        empty_shopping_cart.add_product(sample_product2, -2)

@pytest.mark.parametrize("quantity", [1, 5, 10])
def test_multiple_adding(empty_shopping_cart, sample_product2, quantity):
    empty_shopping_cart.add_product(sample_product2, quantity)
    assert empty_shopping_cart.get_product_count() == quantity


def test_removing_product(filled_cart, sample_product2,sample_product1):
    filled_cart.remove_product(sample_product2.id)
    assert filled_cart.get_product_count() == 6
    assert filled_cart.products[sample_product2.id]["quantity"] == 4
    filled_cart.remove_product(sample_product2.id,3)
    assert filled_cart.get_product_count() == 3
    assert filled_cart.products[sample_product2.id]["quantity"] == 1
    filled_cart.remove_product(sample_product2.id)
    assert sample_product2.id not in filled_cart.products.keys()


def test_removing_non_existing_item(filled_cart):

    with pytest.raises(ValueError):
        filled_cart.remove_product(3)

def test_removing_item_with_negative_quantity(filled_cart, sample_product2):

    with pytest.raises(ValueError):
        filled_cart.remove_product(sample_product2, -2)

def test_total_price(filled_cart, sample_product2):
    assert filled_cart.get_total_price() == 144
    filled_cart.add_product(sample_product2)
    assert filled_cart.get_total_price() == 167
    filled_cart.remove_product(sample_product2.id,3)
    assert filled_cart.get_total_price() == 98


