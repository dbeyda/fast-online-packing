"""Implements a MWU-max method.

    The MWU implemented here tries to maximize a cost function (gains function, in this case).
    This is done by alocating probabilities in the available dimensions, with the constraint that
    the sum of allocated probabilities is <= 1.
"""
from typing import List
import copy


class MwuMax:
    """Class that implements MWU-max algorithm.

    Parameters
    ----------
    n_experts : int
        Dimension of the problem cost function.
    eps : float
        Calibration parameter that regulates the step-size of the updates.

    Methods
    -------
    update_weights(expert_gains: List[float])
        Update mwu probabilities based on a new input of the cost function.
    get_probs()
        Get a copy of the currently allocated probabilities.
    get_n_experts()
        Get the number of dimensions used in this instance.

    Notes
    -----
    Usually, the mwu respects the following restriction: :math:`\\sum_{i=1}^d p_i = 1`, where :math:`p_i` is
    the probability or weight attributed to dimnesion :math:`i`. In order to accomodate the restriction that
    :math:`\\sum_{i=1}^d p_i \\leq 1`, we consider an extra dimension, which always receives cost 0.

    """
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
        # here we use _n_experts+1 because of the extra dimension to transform the
        # equality constraint into <=.
        self._probs = [1/(self._n_experts+1) for _ in range(self._n_experts)]

    def update_weights(self, expert_gains: List[float]) -> List[float]:
        """Update mwu probailitiesbased on a new input of the cost function.

        Parameters
        ----------
        expert_gains : list of float
            A list containing the new input from the cost function. Length must match instance dimension.

        Returns
        -------
        list of float
            Updated probabilies of each dimension.
        """
        assert len(expert_gains) == self._n_experts

        for i in range(self._n_experts):
            self._weights[i] *= (1 + self._eps * expert_gains[i])
        # we sum an extra 1 that is the extra expert weight
        sum_weights = sum(self._weights)+1
        for i in range(self._n_experts):
            self._probs[i] = self._weights[i] / sum_weights
        return copy.copy(self._probs)

    def get_probs(self) -> List[float]:
        """Getter for the current probabilities.

        Returns
        -------
        list of float
            Current probabilies of each dimension.
        """
        return copy.copy(self._probs)

    def get_n_experts(self) -> int:
        """Getter for the number of dimensions (experts) in this instance.

        Returns
        -------
        int
            The number of experts.
        """
        return self._n_experts
