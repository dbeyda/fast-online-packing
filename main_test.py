from online_packing.offline_solvers.google_knapsack_solver import GoogleKnapsackSolver
from online_packing.offline_solvers.python_mip_solver import PythonMIPSolver
from online_packing.instance_generator import generator

t = 50
cost_dim = 3

print("> Testing google solver...")
values, costs, cap = generator.new_packing_problem(
    t, cost_dim, itens_per_instant=1, mandatory_packing=False)
s = GoogleKnapsackSolver(values, costs, cap)
s.solve()
s.print_result()
print("> Ok.")

print("\n> Testing Python-MIP solver...")
# p = generator.new_packing_problem(t, cost_dim, itens_per_instant=5, mandatory_packing=False)
s = PythonMIPSolver(values, costs, cap)
s.solve()
s.print_result()
print("> Ok.")
