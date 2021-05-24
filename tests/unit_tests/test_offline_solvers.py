from typing import Any
import pytest
from fast_online_packing.offline_solvers.google_knapsack_solver import GoogleKnapsackSolver
from fast_online_packing.offline_solvers.python_mip_solver import PythonMIPSolver


example1: Any = {
    "values": [
        [360.0], [83.0], [59.0], [130.0], [431.0], [67.0],
        [230.0], [52.0], [93.0], [125.0], [670.0], [892.0],
        [600.0], [38.0], [48.0], [147.0], [78.0], [256.0],
        [63.0], [17.0], [120.0], [164.0], [432.0], [35.0],
        [92.0], [110.0], [22.0], [42.0], [50.0], [323.0],
        [514.0], [28.0], [87.0], [73.0], [78.0], [15.0],
        [26.0], [78.0], [210.0], [36.0], [85.0], [189.0],
        [274.0], [43.0], [33.0], [10.0], [19.0], [389.0],
        [276.0], [312.0]
    ],
    "weights": [
        [[7.0]], [[0.0]], [[30.0]], [[22.0]], [[80.0]],
        [[94.0]], [[11.0]], [[81.0]], [[70.0]], [[64.0]],
        [[59.0]], [[18.0]], [[0.0]], [[36.0]], [[3.0]],
        [[8.0]], [[15.0]], [[42.0]], [[9.0]], [[0.0]],
        [[42.0]], [[47.0]], [[52.0]], [[32.0]], [[26.0]],
        [[48.0]], [[55.0]], [[6.0]], [[29.0]], [[84.0]],
        [[2.0]], [[4.0]], [[18.0]], [[56.0]], [[7.0]],
        [[29.0]], [[93.0]], [[44.0]], [[71.0]], [[3.0]],
        [[86.0]], [[66.0]], [[31.0]], [[65.0]], [[0.0]],
        [[79.0]], [[20.0]], [[65.0]], [[52.0]], [[13.0]]
    ],
    "cap": 850.0,
    "result": 7534.0
}

example2: Any = {
    "values": [
        [5.0], [1.0], [1.0], [1.1], [1.0], [1.0],
        [1.0], [1.1], [1.2], [1.3], [1.0], [1.0]
    ],
    "weights": [
        [[5.0]], [[1.0]], [[1.0]], [[1.0]], [[1.0]],
        [[1.0]], [[1.0]], [[1.0]], [[1.0]], [[1.0]],
        [[1.0]], [[1.0]]
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


class TestPythonMipSolver:
    def test_examples(self):
        for e in ex:
            s = PythonMIPSolver(e["values"], e["weights"], e["cap"])
            s.solve()
            expected = e["result"]
            assert (expected - 1e-6) <= s.optimum_value <= (expected + 1e-6)
