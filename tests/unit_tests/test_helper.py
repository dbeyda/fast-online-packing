from typing import Any
import pytest
from online_packing import helper


class TestDotProduct:
    def test_integer_inputs(self):
        a: Any = [1, 2, 3]
        b: Any = [4, 5, 6]
        c = helper.dot_product(a, b)
        assert c == 32

    def test_mixed_inputs(self):
        a: Any = [1.0, 2, 3]
        b: Any = [4, 5.0, 6]
        c = helper.dot_product(a, b)
        assert c == 32

    def test_wrong_input(self):
        a: Any = [1.0, 2, 3, 3]
        b: Any = [4, 5.0, 6]
        with pytest.raises(Exception):
            helper.dot_product(a, b)
