Quickstart
==========

|

First, we start by importing our `generator`, that will
generate example instances for us, and the `OnlineSolver`.

.. code-block:: python

    from online_packing import instance_generator as generator
    from online_packing.online_solver import OnlineSolver

    n_instants = 400
    cost_dim = 5

We also set the total number of instants (rounds) to 400,
and the cost dimension to 5. This means our cost vectors will have
a length of 5.

|

Ok. Lets generate an example of the Packing LP problem, and then feed it
to the solver.

.. code-block:: python

    delta = 0.3
    values, costs, cap, e = generator.generate_valid_instance(
        delta, n_instants, cost_dim, items_per_instant=3)

    s = OnlineSolver(cost_dim, n_instants, cap, e)

On the example generation, notice the following:

- `items_per_instant = 3`: this means on each instant or round, there will be 3 options available for the user/algorithm to choose from.

|

Great! Now lets solve the instance in an online fashion:

.. code-block:: python

    print("\n>> Online solver parameters:")
    s.print_params()
    print("\n")

    # play the game, round by round
    for v, c in zip(values, costs):
        s.pack_one(v, c)

    # check and compare against the offline optimum
    s.compute_optimum()
    s.print_result()
    if not s.respect_premises():
        print("\n! OBS ! constrains violated.")

The output should be similary to:

.. code-block:: none

    Online solver parameters:
    capacity = 285
    cost dimension = 5
    e = 0.07514752537472016
    delta = 0.2998953403788148
    initial phase size = 120
    total time = 400


    Opt: 298.1102216801745
    Alg: 249.78456377970605
    Score Alg = 0.838 * Opt
        min {B, TOPT} = 285.000
        B = 285
        TOPT = 298.1102216801745

Wow! Take a look at that! We used 30% of the instants to estimate algorithm
parameters (Z), choosing randomly at those instants, and still managed to make
83.4% of the optimum in an online way! Very impressive.

Thanks to Agrawal and Devanur's "Fast Algorithms for Online Stochastic Convex Programming"!

|

**Disclaimer about theoretical guarantees**: It is possible that some of the premises for the algorithm are violated.
In that case, the excelent theoretical guarantees we counted on here are not valid.
That's what the last lines of the code and output are for. Sadly, one of the premises
depends on the offline optimum, meaning we can only find out if the algorithm fulfilled
it's premises *after* we end all the rounds, because this check will require us to
compute the offline optimum. 

|

Full code below:

.. code-block:: python

    from online_packing import instance_generator as generator
    from online_packing.online_solver import OnlineSolver

    n_instants = 400
    cost_dim = 5

    delta = 0.3
    values, costs, cap, e = generator.generate_valid_instance(
        delta, n_instants, cost_dim, items_per_instant=3)

    s = OnlineSolver(cost_dim, n_instants, cap, e, PythonMIPSolver)

    print("\n>> Online solver parameters:")
    s.print_params()

    for v, c in zip(values, costs):
        s.pack_one(v, c)

    s.compute_optimum()
    s.print_result()
    if not s.respect_premises():
        print("\n! OBS ! constrains violated.")

