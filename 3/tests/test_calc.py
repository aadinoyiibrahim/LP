import pytest
from calc import add, subtract, multiply

@pytest.mark.parametrize("x,y,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-5, 5, 0),
])
def test_add(x, y, expected):
    assert add(x, y) == expected


@pytest.mark.parametrize("x,y,expected", [
    (5, 2, 3),
    (0, 0, 0),
    (2, -2, 4),
])
def test_subtract(x, y, expected):
    assert subtract(x, y) == expected


@pytest.mark.parametrize("x,y,expected", [
    (2, 3, 6),
    (0, 5, 0),
    (-2, -3, 6),
])
def test_multiply(x, y, expected):
    assert multiply(x, y) == expected
