from online_packing.instance_generator.generator import generate_random_instance, generate_valid_instance
import pytest
from math import log


class TestGenerateRandomInstance:
    def test_wrong_params(self):
        with pytest.raises(Exception):
            generate_random_instance(15, 0, 3)
        with pytest.raises(Exception):
            generate_random_instance(15, 3, 0)

    def test_mandatory_true(self):
        _, c, _, _ = generate_random_instance(10, 3, 3, True)
        for day in c:
            for dim in day[-1]:
                if not (-1e-6 <= dim <= 1e-6):
                    break  # passed test

    def test_mandatory_false(self):
        v, c, _, _ = generate_random_instance(10, 3, 3, False)
        for day in c:
            for dim in day[-1]:
                assert (-1e-6 <= dim <= 1e-6)
        for day in v:
            assert -1e-6 <= day[-1] <= 1e-6


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

    def test_mandatory_true(self):
        _, c, _, _ = generate_valid_instance(0.2, 10, 3, 3, True)
        for day in c:
            for dim in day[-1]:
                if not (-1e-6 <= dim <= 1e-6):
                    break  # passed test

    def test_mandatory_false(self):
        v, c, _, _ = generate_valid_instance(0.2, 10, 3, 3, False)
        for day in c:
            for dim in day[-1]:
                assert (-1e-6 <= dim <= 1e-6)
        for day in v:
            assert -1e-6 <= day[-1] <= 1e-6

    def test_constaints(self):
        target_delta = 0.2
        cost_dim = 3
        _, _, cap, e = generate_valid_instance(target_delta, 10, 3, 3)
        delta = (12 / cap) * log((cost_dim+2)*cap / log(cost_dim))
        assert e <= 0.5-1e-6
        assert delta - 1e-6 <= target_delta
