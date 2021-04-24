from online_packing.offline_solvers.google_knapsack_solver import GoogleKnapsackSolver
from online_packing.offline_solvers.python_mip_solver import PythonMIPSolver
from online_packing.instance_generator import generator
from online_packing.online_solver import OnlineSolver
from math import log, sqrt

# t = 50
# cost_dim = 3
# print("> Testing solvers...")
# print(">> Testing google solver...")
# values, costs, cap = generator.new_packing_problem(
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
    t, cost_dim, items_per_instant=3, mandatory_packing=False)

e = sqrt(log(cost_dim, 2)/cap)
min_bopt = log(cost_dim) / (e*e)
print(f"Cap = {cap}")

s = OnlineSolver(e, len(costs[0][0]), len(values), cap, PythonMIPSolver)
print("\n>> Testing online algorithm with parameters:")
s.print_params()
for v, c in zip(values, costs):
    s.pack_one(v, c)
print(f"> Opt: {s.compute_optimum()}")
print(f"> Alg: {s.p._packed_value_sum}")  # type: ignore
print(f"Score Alg = {s.p._packed_value_sum/s.optimum_value :.3f} * Opt")  # type: ignore
print(f"     min {{B, TOPT}} = {min_bopt}")
print(f"     B = {cap}")
print(f"     TOPT = {s.optimum_value}")
if cap < min_bopt or s.optimum_value < min_bopt:
    print("\n! OBS ! constrains violated:")
