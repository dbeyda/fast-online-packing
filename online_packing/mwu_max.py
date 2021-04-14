from typing import List
import copy


class MwuMax:
    _n_experts: int
    _eps: float
    _weights: List[float]
    _probs: List[float]

    def __init__(self, n_experts: int, eps: float):
        assert n_experts > 0
        assert eps > 1e-6
        assert eps < 0.5-1e-6

        self._n_experts = n_experts
        self._eps = eps
        self._weights = [1 for _ in range(self._n_experts)]
        self._probs = [1/(self._n_experts+1) for _ in range(self._n_experts)]

    def update_weights(self, expert_gains: List[float]):
        assert len(expert_gains) == self._n_experts

        for i in range(self._n_experts):
            self._weights[i] *= (1 + self._eps * expert_gains[i])
        sum_weights = sum(self._weights)+1
        for i in range(self._n_experts):
            self._probs[i] = self._weights[i] / sum_weights
        return copy.copy(self._probs)

    def get_probs(self):
        return copy.copy(self._probs)
