from online_packing.offline_solvers.google_knapsack_solver import GoogleKnapsackSolver
from online_packing.offline_solvers.python_mip_solver import PythonMIPSolver
from online_packing.instance_generator import generator
from online_packing.online_solver import OnlineSolver

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
cost_dim = 5

values, costs, cap, e = generator.generate_valid_instance(
    0.3, t, cost_dim, items_per_instant=3, mandatory_packing=False)

s = OnlineSolver(cost_dim, t, cap, e, PythonMIPSolver)
print("\n>> Testing online algorithm with parameters:")
s.print_params()
for v, c in zip(values, costs):
    s.pack_one(v, c)
print(f"z set to {s.z}")
s.compute_optimum()
s.print_result()
if not s.respect_premises():
    print("\n! OBS ! constrains violated.")
