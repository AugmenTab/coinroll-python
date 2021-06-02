#! python3

from main import add


def test_add():
    assert add(4,5) == 9


if __name__ == '__main__':
    test_add()
