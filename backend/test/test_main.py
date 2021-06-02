#! python3

# 3p Imports
import pytest

# Internal Imports
from src.main import add


def test_add():
    assert add(4, 5) == 9
    assert add(3, 1) != 5
