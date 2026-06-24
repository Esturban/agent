from calculator import add, multiply


def test_add():
    assert add(2, 3) == 5  # FAILS: add() subtracts


def test_multiply():
    assert multiply(3, 4) == 12
