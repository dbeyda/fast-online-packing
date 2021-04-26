from online_packing.offline_solvers.google_knapsack_solver import GoogleKnapsackSolver
from online_packing.offline_solvers.python_mip_solver import PythonMIPSolver
from online_packing.instance_generator import generator
from online_packing.online_solver import OnlineSolver
from math import log, sqrt

# t = 50
# cost_dim = 3
# print("> Testing solvers...")
# print(">> Testing google solver...")
# values, costs, cap, _ = generator.generate_random_instance(
#     t, cost_dim, items_per_instant=1, mandatory_packing=False)
# s = GoogleKnapsackSolver(values, costs, cap)
# s.solve()
# s.print_result()
# print(">> Ok.")

# print("\n>> Testing Python-MIP solver...")
# s = PythonMIPSolver(values, costs, cap)
# s.solve()
# s.print_result()
# print(">> Ok.")

t = 400
cost_dim = 4

values, costs, cap, e = generator.generate_valid_instance(
    0.3, t, cost_dim, items_per_instant=3, mandatory_packing=False)

s = OnlineSolver(e, len(costs[0][0]), len(values), cap, PythonMIPSolver)
print("\n>> Testing online algorithm with parameters:")
s.print_params()
for v, c in zip(values, costs):
    s.pack_one(v, c)
print(f"z set to {s.z}")
print(f"> Opt: {s.compute_optimum()}")
print(f"> Alg: {s.p._packed_value_sum}")  # type: ignore
print(f"Score Alg = {s.p._packed_value_sum/s.optimum_value :.3f} * Opt")  # type: ignore
print(f"     min {{B, TOPT}} = {s.get_premises_min()}")
print(f"     B = {cap}")
print(f"     TOPT = {s.optimum_value}")
if not s.respect_premises():
    print("\n! OBS ! constrains violated.")
