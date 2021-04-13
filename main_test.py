from online_packing.offline_solvers.google_solver import GoogleSolver
from online_packing.offline_solvers.python_mip_solver import PythonMIPSolver
from online_packing.instance_generator import generator

t = 50
cost_dim = 3

print("> Testing google solver...")
p = generator.new_packing_problem(t, cost_dim, itens_per_instant=1, mandatory_packing=False)
s = GoogleSolver(p)
s.solve()
s.print_result()
print("> Ok.")

print("\n> Testing Python-MIP solver...")
# p = generator.new_packing_problem(t, cost_dim, itens_per_instant=5, mandatory_packing=False)
s = PythonMIPSolver(p)
s.solve()
s.print_result()
print("> Ok.")
