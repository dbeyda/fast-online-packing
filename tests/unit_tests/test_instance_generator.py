from online_packing.instance_generator.generator import new_packing_problem
import pytest


class TestNewPackingProblem:
    def test_wrong_params(self):
        with pytest.raises(Exception):
            new_packing_problem(15, 0, 3)
        with pytest.raises(Exception):
            new_packing_problem(15, 3, 0)

    def test_mandatory_true(self):
        _, c, _ = new_packing_problem(10, 3, 3, True)
        for day in c:
            for dim in day[-1]:
                if not (-1e-6 <= dim <= 1e-6):
                    break  # passed test

    def test_mandatory_false(self):
        v, c, _ = new_packing_problem(10, 3, 3, False)
        for day in c:
            for dim in day[-1]:
                assert (-1e-6 <= dim <= 1e-6)
        for day in v:
            assert -1e-6 <= day[-1] <= 1e-6
