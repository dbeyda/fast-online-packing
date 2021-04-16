from typing import Any
import pytest
from online_packing.offline_solvers.google_knapsack_solver import GoogleKnapsackSolver
from online_packing.offline_solvers.python_mip_solver import PythonMIPSolver


example1: Any = {
    "values": [
        [360.0, 0.0], [83.0, 0.0], [59.0, 0.0], [130.0, 0.0], [431.0, 0.0], [67.0, 0.0],
        [230.0, 0.0], [52.0, 0.0], [93.0, 0.0], [125.0, 0.0], [670.0, 0.0], [892.0, 0.0],
        [600.0, 0.0], [38.0, 0.0], [48.0, 0.0], [147.0, 0.0], [78.0, 0.0], [256.0, 0.0],
        [63.0, 0.0], [17.0, 0.0], [120.0, 0.0], [164.0, 0.0], [432.0, 0.0], [35.0, 0.0],
        [92.0, 0.0], [110.0, 0.0], [22.0, 0.0], [42.0, 0.0], [50.0, 0.0], [323.0, 0.0],
        [514.0, 0.0], [28.0, 0.0], [87.0, 0.0], [73.0, 0.0], [78.0, 0.0], [15.0, 0.0],
        [26.0, 0.0], [78.0, 0.0], [210.0, 0.0], [36.0, 0.0], [85.0, 0.0], [189.0, 0.0],
        [274.0, 0.0], [43.0, 0.0], [33.0, 0.0], [10.0, 0.0], [19.0, 0.0], [389.0, 0.0],
        [276.0, 0.0], [312.0, 0.0]
    ],
    "weights": [
        [[7.0], [0.0]], [[0.0], [0.0]], [[30.0], [0.0]], [[22.0], [0.0]], [[80.0], [0.0]],
        [[94.0], [0.0]], [[11.0], [0.0]], [[81.0], [0.0]], [[70.0], [0.0]], [[64.0], [0.0]],
        [[59.0], [0.0]], [[18.0], [0.0]], [[0.0], [0.0]], [[36.0], [0.0]], [[3.0], [0.0]],
        [[8.0], [0.0]], [[15.0], [0.0]], [[42.0], [0.0]], [[9.0], [0.0]], [[0.0], [0.0]],
        [[42.0], [0.0]], [[47.0], [0.0]], [[52.0], [0.0]], [[32.0], [0.0]], [[26.0], [0.0]],
        [[48.0], [0.0]], [[55.0], [0.0]], [[6.0], [0.0]], [[29.0], [0.0]], [[84.0], [0.0]],
        [[2.0], [0.0]], [[4.0], [0.0]], [[18.0], [0.0]], [[56.0], [0.0]], [[7.0], [0.0]],
        [[29.0], [0.0]], [[93.0], [0.0]], [[44.0], [0.0]], [[71.0], [0.0]], [[3.0], [0.0]],
        [[86.0], [0.0]], [[66.0], [0.0]], [[31.0], [0.0]], [[65.0], [0.0]], [[0.0], [0.0]],
        [[79.0], [0.0]], [[20.0], [0.0]], [[65.0], [0.0]], [[52.0], [0.0]], [[13.0], [0.0]]
    ],
    "cap": 850.0,
    "result": 7534.0
}

example2: Any = {
    "values": [
        [5.0, 0.0], [1.0, 0.0], [1.0, 0.0], [1.1, 0.0], [1.0, 0.0], [1.0, 0.0],
        [1.0, 0.0], [1.1, 0.0], [1.2, 0.0], [1.3, 0.0], [1.0, 0.0], [1.0, 0.0]
    ],
    "weights": [
        [[5.0], [0.0]], [[1.0], [0.0]], [[1.0], [0.0]], [[1.0], [0.0]], [[1.0], [0.0]],
        [[1.0], [0.0]], [[1.0], [0.0]], [[1.0], [0.0]], [[1.0], [0.0]], [[1.0], [0.0]],
        [[1.0], [0.0]], [[1.0], [0.0]]
    ],
    "cap": 5.0,
    "result": 5.7
}

ex = [example1, example2]


class TestGoogleKnapsackSolver:
    def test_examples(self):
        for e in ex:
            s = GoogleKnapsackSolver(e["values"], e["weights"], e["cap"])
            s.solve()
            expected = e["result"]
            assert (expected - 1e-6) <= s.optimum_value <= (expected + 1e-6)

    def test_mandatory_packing(self):
        v: Any = [[1], [2], [3]]
        c: Any = [[[1]], [[1]], [[1]]]
        with pytest.raises(Exception):
            s = GoogleKnapsackSolver(v, c, 200)
            s.solve()


class TestPythonMipSolver:
    def test_examples(self):
        for e in ex:
            s = PythonMIPSolver(e["values"], e["weights"], e["cap"])
            s.solve()
            expected = e["result"]
            assert (expected - 1e-6) <= s.optimum_value <= (expected + 1e-6)
