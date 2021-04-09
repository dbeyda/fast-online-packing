from abc import ABC, abstractmethod
from online_packing.packing_problem import PackingProblem


class BaseSolver(ABC):
    problem: PackingProblem

    def __init__(self, p: PackingProblem):
        self.problem = p

    @abstractmethod
    def solve(self) -> None:
        pass

    @abstractmethod
    def print_result(self) -> None:
        pass
