from fast_online_packing.instance_generator import generate_random_instance, generate_valid_instance
import pytest
from math import log


class TestGenerateRandomInstance:
    def test_wrong_params(self):
        with pytest.raises(Exception):
            generate_random_instance(15, 0, 3)
        with pytest.raises(Exception):
            generate_random_instance(15, 3, 0)

    def test_generate_instance(self):
        v, c, _, _ = generate_random_instance(10, 3, 3)
        assert len(v) == len(c) == 10
        assert len(c[0]) == 3
        assert len(v[0]) == 3


class TestGenerateValidInstance:
    def test_wrong_params(self):
        with pytest.raises(Exception):
            generate_valid_instance(-1, 5, 2, 2)
        with pytest.raises(Exception):
            generate_valid_instance(3, 5, 2, 2)
        with pytest.raises(Exception):
            generate_valid_instance(0.2, 15, 0, 3)
        with pytest.raises(Exception):
            generate_valid_instance(0.2, 15, 3, 0)

    def test_generate_instance(self):
        v, c, _, _ = generate_valid_instance(0.2, 10, 3, 3)
        assert len(v) == len(c) == 10
        assert len(c[0]) == 3
        assert len(v[0]) == 3

    def test_constaints(self):
        target_delta = 0.2
        cost_dim = 3
        _, _, cap, e = generate_valid_instance(target_delta, 10, 3, 3)
        delta = (12 / cap) * log((cost_dim+2)*cap / log(cost_dim))
        assert e <= 0.5-1e-6
        assert delta - 1e-6 <= target_delta
