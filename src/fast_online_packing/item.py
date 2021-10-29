from typing import List, Union


class Item:
    _costs: List[float]
    _reward: float

    def __init__(self, reward: Union[int, float], costs: List[Union[int, float]]):
        self._reward = float(reward)
        self._costs = [float(c) for c in costs]

    @property
    def reward(self) -> float:
        return self._reward

    @property
    def costs(self) -> List[float]:
        return self._costs

    @property
    def cost_dim(self) -> int:
        return len(self._costs)
