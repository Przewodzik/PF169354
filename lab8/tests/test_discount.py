import pytest
from lab8.src.discount import calculate_discounted_price


def test_calculate_discounted_price_positive():

    assert calculate_discounted_price(100,0) == 100
    assert calculate_discounted_price(100,40) == 60
    assert calculate_discounted_price(100,100) == 0
    assert calculate_discounted_price(100,10) == 90

def test_calculate_discounted_price_negative():

    assert calculate_discounted_price(100, 40) != 50
    assert calculate_discounted_price(40.22, 2.33) != 20.33

def test_invalid_discount():

    with pytest.raises(ValueError):
        calculate_discounted_price(100,"discount")

    with pytest.raises(ValueError):
        calculate_discounted_price(100,-100)

def test_invalid_price():
    with pytest.raises(ValueError):
        calculate_discounted_price("price",10)

    with pytest.raises(ValueError):
        calculate_discounted_price(-100,10)


def test_rounding():

    assert calculate_discounted_price(100, 33.33) == 66.67
    assert calculate_discounted_price(100, 66.66) == 33.34
    assert calculate_discounted_price(9.99, 10) == 8.99


