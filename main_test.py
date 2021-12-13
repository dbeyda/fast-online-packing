from fast_online_packing.offline_solvers.google_knapsack_solver import GoogleKnapsackSolver
from fast_online_packing.offline_solvers.python_mip_solver import PythonMIPSolver
from fast_online_packing import instance_generator as generator
from fast_online_packing.online_solver import OnlineSolver

# t = 50
# cost_dim = 3
# print("> Testing solvers...")
# print(">> Testing google solver...")
# values, costs, cap, _ = generator.generate_random_instance(
#     t, cost_dim, items_per_instant=1)
# s = GoogleKnapsackSolver(values, costs, cap)
# s.solve()
# s.print_result()
# print(">> Ok.")

# print("\n>> Testing Python-MIP solver...")
# s = PythonMIPSolver(values, costs, cap)
# s.solve()
# s.print_result()
# print(">> Ok.")

n_instants = 400
cost_dim = 3

values, costs, cap, e = generator.generate_valid_instance(
    0.3, n_instants, cost_dim, items_per_instant=3)

s = OnlineSolver(cost_dim, n_instants, cap, 0.08, PythonMIPSolver)

for v, c in zip(values, costs):
    s.pack_one(v, c)
s.compute_optimum()

print("\nOnline solver parameters:")
s.print_params()
print("\n")

s.print_result()
