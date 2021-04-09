from online_packing.solver import GooglePackingSolver
from online_packing.instance_generator import generator

t = 50
cost_dim = 3
p = generator.new_packing_problem(t, cost_dim, itens_per_instant=1, mandatory_packing=True)
g = GooglePackingSolver(p)
g.solve()
g.print_result()
