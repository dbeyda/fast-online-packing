import pytest
from online_packing import packing_problem


class TestPackingProblem:
    def test_create(self):
        with pytest.raises(Exception):
            packing_problem.PackingProblem(-3, 5)
        with pytest.raises(Exception):
            packing_problem.PackingProblem(1, 0)
        with pytest.raises(Exception):
            packing_problem.PackingProblem(1, -1)

    def test_get_capacity(self):
        p = packing_problem.PackingProblem(25.5, 5)
        assert 25.5 - 1e-6 <= p.get_capacity() <= 25.5 + 1e-6
        p = packing_problem.PackingProblem(3, 5)
        assert p.get_capacity() == 3

    def test_get_cost_dimension(self):
        p = packing_problem.PackingProblem(25.5, 5)
        assert p.get_cost_dimension() == 5

    def test_set_current_inputs(self):
        problem_instance = packing_problem.PackingProblem(0.5, 2)
        # test raise exception
        with pytest.raises(Exception):
            problem_instance.set_current_inputs([0.8], [[0.4, 1.2]])
        with pytest.raises(Exception):
            problem_instance.set_current_inputs([0.8], [[-0.4, 0.2]])
        # test expected behaviour
        problem_instance.set_current_inputs([0.8], [[0.4, 0.2]])
        assert problem_instance.get_available_costs() == [[[0.4, 0.2]]]
        assert problem_instance.get_available_values() == [[0.8]]
        assert problem_instance.get_options_per_instant() == 1

    def test_two_inputs_in_a_row(self):
        problem_instance = packing_problem.PackingProblem(0.5, 2)
        # test setting two inputs in a row raises exception
        problem_instance.set_current_inputs([0.0], [[0.0, 0.0]])
        with pytest.raises(Exception):
            problem_instance.set_current_inputs([0.0], [[0.0, 0.0]])

    def test_item_fits(self):
        # truthy input 1
        problem_instance = packing_problem.PackingProblem(0.5, 2)
        problem_instance.set_current_inputs([0.8], [[0.4, 0]])
        assert problem_instance.item_fits(0) is True
        # truthy input 2
        problem_instance = packing_problem.PackingProblem(0.5, 2)
        problem_instance.set_current_inputs([0.8], [[0.4, 0.3]])
        assert problem_instance.item_fits(0) is True
        # falsy input
        problem_instance = packing_problem.PackingProblem(0.5, 2)
        problem_instance.set_current_inputs([0.8], [[0.6, 0]])
        assert problem_instance.item_fits(0) is False

    def test_pack_item(self):
        p = packing_problem.PackingProblem(0.5, 2)
        p.set_current_inputs([0.3, 0.4], [[0.1, 0.2], [0.5, 0.6]])
        # test packing doesnt fit
        with pytest.raises(Exception):
            p.pack(1)
        p.pack(0)

    def test_pack_none(self):
        p = packing_problem.PackingProblem(0.01, 2)
        p.set_current_inputs([0.3, 0.4], [[0.1, 0.2], [0.5, 0.6]])
        p.pack(-1)

    def test_packing_two_in_a_row(self):
        p = packing_problem.PackingProblem(0.5, 2)
        p.set_current_inputs([0.3, 0.4], [[0.1, 0.2], [0.5, 0.6]])
        p.pack(0)
        # test has to set_inputs first
        with pytest.raises(Exception):
            p.pack(1)
        # test item 0 doesnt fit
        p.set_current_inputs([0.3, 0.4], [[0.1, 0.4], [0.4, 0.3]])
        with pytest.raises(Exception):
            p.pack(0)
        # test item 1 does fit
        p.pack(1)
