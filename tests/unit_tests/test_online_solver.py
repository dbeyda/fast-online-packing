from online_packing.online_solver import OnlineSolver
from test_data import instance_valid_premises, instance_violated_premises

valid = instance_valid_premises
violated = instance_violated_premises


class TestOnlineSolver():
    def test_pack_one(self):
        s = OnlineSolver(valid["cost_dim"], valid["n_instants"], valid["cap"], valid["e"])
        for v, c in zip(valid["values"], valid["costs"]):
            s.pack_one(v, c)

        ss = OnlineSolver(violated["cost_dim"], violated["n_instants"], violated["cap"], violated["e"])
        for v, c in zip(violated["values"], violated["costs"]):
            ss.pack_one(v, c)

    def test_compute_optimum(self):
        s = OnlineSolver(valid["cost_dim"], valid["n_instants"], valid["cap"], valid["e"])
        for v, c in zip(valid["values"], valid["costs"]):
            s.pack_one(v, c)
        s.compute_optimum()

        ss = OnlineSolver(violated["cost_dim"], violated["n_instants"], violated["cap"], violated["e"])
        for v, c in zip(violated["values"], violated["costs"]):
            ss.pack_one(v, c)
        ss.compute_optimum()

    def test_get_premises_min(self):
        s = OnlineSolver(valid["cost_dim"], valid["n_instants"], valid["cap"], valid["e"])
        for v, c in zip(valid["values"], valid["costs"]):
            s.pack_one(v, c)
        s.compute_optimum()
        assert s.get_premises_min() < valid["premises_min"]+0.1
        assert s.get_premises_min() > valid["premises_min"]-0.1

        ss = OnlineSolver(violated["cost_dim"], violated["n_instants"], violated["cap"], violated["e"])
        for v, c in zip(violated["values"], violated["costs"]):
            ss.pack_one(v, c)
        ss.compute_optimum()
        assert ss.get_premises_min() < violated["premises_min"]+0.1
        assert ss.get_premises_min() > violated["premises_min"]-0.1

    def test_respect_premises(self):
        s = OnlineSolver(valid["cost_dim"], valid["n_instants"], valid["cap"], valid["e"])
        for v, c in zip(valid["values"], valid["costs"]):
            s.pack_one(v, c)
        s.compute_optimum()
        assert s.respect_premises() is True

        ss = OnlineSolver(violated["cost_dim"], violated["n_instants"], violated["cap"], violated["e"])
        for v, c in zip(violated["values"], violated["costs"]):
            ss.pack_one(v, c)
        ss.compute_optimum()
        assert ss.respect_premises() is False
