from online_packing.offline_solvers.google_knapsack_solver import GoogleKnapsackSolver
from online_packing.offline_solvers.python_mip_solver import PythonMIPSolver
from online_packing.instance_generator import generator
from online_packing.online_solver import OnlineSolver

t = 50
cost_dim = 3
print("> Testing solvers...")
print(">> Testing google solver...")
values, costs, cap = generator.new_packing_problem(
    t, cost_dim, itens_per_instant=1, mandatory_packing=False)
s = GoogleKnapsackSolver(values, costs, cap)
s.solve()
s.print_result()
print(">> Ok.")

print("\n>> Testing Python-MIP solver...")
s = PythonMIPSolver(values, costs, cap)
s.solve()
s.print_result()
print(">> Ok.")

t = 100
cost_dim = 2
values, costs, cap = generator.new_packing_problem(
    t, cost_dim, itens_per_instant=3, mandatory_packing=False)
s = OnlineSolver(0.1, len(costs[0][0]), len(values), 35)
print("\n>> Testing online algorithm with parameters:")
s.print_params()
for v, c in zip(values, costs):
    s.pack_one(v, c)
print(f"> Opt: {s.compute_optimum()}")
print(f"> Alg: {s.p._packed_value_sum}")
