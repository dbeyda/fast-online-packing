from online_packing.offline_solvers.google_knapsack_solver import GoogleKnapsackSolver
from online_packing.offline_solvers.python_mip_solver import PythonMIPSolver
from online_packing.instance_generator import generator
from online_packing.online_solver import OnlineSolver
from math import log

# t = 50
# cost_dim = 3
# print("> Testing solvers...")
# print(">> Testing google solver...")
# values, costs, cap = generator.new_packing_problem(
#     t, cost_dim, itens_per_instant=1, mandatory_packing=False)
# s = GoogleKnapsackSolver(values, costs, cap)
# s.solve()
# s.print_result()
# print(">> Ok.")

# print("\n>> Testing Python-MIP solver...")
# s = PythonMIPSolver(values, costs, cap)
# s.solve()
# s.print_result()
# print(">> Ok.")

t = 300
cost_dim = 2
e = 0.1
min_bopt = log(cost_dim) / (e*e)

values, costs, cap = generator.new_packing_problem(
    t, cost_dim, itens_per_instant=3, mandatory_packing=False)

cap = log(cost_dim)/(e * e) + 10
cap = 300
print(f"Cap = {cap}")

s = OnlineSolver(0.1, len(costs[0][0]), len(values), 35, PythonMIPSolver)
print("\n>> Testing online algorithm with parameters:")
s.print_params()
for v, c in zip(values, costs):
    s.pack_one(v, c)
print(f"> Opt: {s.compute_optimum()}")
print(f"> Alg: {s.p._packed_value_sum}")  # type: ignore
if cap < min_bopt or s.optimum_value < min_bopt:
    print("\n! OBS ! constrains violated:")
    print(f"     min {{B, TOPT}} = {min_bopt}")
    print(f"     B = {cap}")
    print(f"     TOPT = {s.optimum_value}")
