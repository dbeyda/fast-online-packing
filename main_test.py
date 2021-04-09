from online_packing.solver import GooglePackingSolver
from online_packing.instance_generator import generator

t = 50
cost_dim = 5
p = generator.new_packing_problem(t, cost_dim)
g = GooglePackingSolver(p)
g.solve()
g.print_result()
