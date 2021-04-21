import pytest
from online_packing.mwu_max import MwuMax


class TestMwuMax():
    def test_zero_experts(self):
        with pytest.raises(Exception):
            MwuMax(0, 0.1)

    def test_negative_experts(self):
        with pytest.raises(Exception):
            MwuMax(-2, 0.1)

    def test_eps_inferior_range(self):
        with pytest.raises(Exception):
            MwuMax(3, 0)

    def test_eps_superior_range(self):
        with pytest.raises(Exception):
            MwuMax(3, 0.6)

    def test_wrong_weights(self):
        m = MwuMax(3, 0.1)
        with pytest.raises(Exception):
            m.update_weights([0.5, 0.5, -0.1, -0.1])

    def test_get_n_experts(self):
        m = MwuMax(3, 0.1)
        assert m.get_n_experts() == 3

    def test_get_probs(self):
        m = MwuMax(3, 0.1)
        m.update_weights([0.5, 0.5, -0.1])
        p = m.get_probs()
        assert len(p) == m.get_n_experts()
        p.append(2)
        assert len(m.get_probs()) == m.get_n_experts()
