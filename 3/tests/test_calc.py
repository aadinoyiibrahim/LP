import pytest
from calc import add, subtract, multiply

@pytest.mark.parametrize("x,y,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-5, 5, 0),
])  # Fixed: Added missing closing bracket
def test_add(x, y, expected):
    assert add(x, y) == expected  # Fixed: Added indentation

@pytest.mark.parametrize("x,y,expected", [
    (5, 2, 3),
    (0, 0, 0),
    (2, -2, 4),  # Note: 2 - (-2) should be 4, not subtract(2, -2) which would be 4
])  # Fixed: Added missing closing bracket
def test_subtract(x, y, expected):
    assert subtract(x, y) == expected  # Fixed: Added indentation

@pytest.mark.parametrize("x,y,expected", [
    (2, 3, 6),
    (0, 5, 0),
    (-2, -3, 6),
])  # Fixed: Cleaned up multiply test cases
def test_multiply(x, y, expected):
    assert multiply(x, y) == expected  # Fixed: Added indentation