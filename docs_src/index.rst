Welcome to Fast Online Packing's API Reference!
===============================================

This package aims to solve the Online Stochastic Packing Problem,
based on the algorithm given by Agrawal and Devanur [1]_.

What is an Online Stochastic Packing Problem?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Introducing the Knapsack Problem.** If you are here, you probably heard of the `Knapsack Problem`_: given a set of
items (each one with it's own value and weight), choose which items to pack
in order to maximize the value that fits the backpack's weight restriction.
Notice each item has a value and a "cost", which we have a restriction on.
On this variation of the problem, there is only one unit of each item for you
to pack (0-1 Knapsack Problem). Ok?

**Get Multidimensional**. Now let's get into the Multidimensional Knapsack Problem: it's the same as the above,
but the items cost is now a vector, meaning the cost has more than one dimension.
You can interpret this as "the backpack is 2D now", or as two separate restrictions:
one for the weight, another on the item prices, because your budget is limited.
Notice the cost vector can have any positive number of dimensions, but it's still a vector.

**What about the Online part?** A problem is called online when you have limited information about
the problem and you have to make a choice using only the little information you have. In the
future, more information will be revealed, you will be asked to make other choices, but past choices cannot be changed.

**The complete picture**. The problem develops in rounds. On each round, you will be
presented `k` items (each one has a value and a cost vector). You have to choose if you want
to pack an item, and which one do you want to pack. You have a capacity `B` in every cost dimension.
The objective is to maximize the packed value, without exceeding the capacity `B` in
any dimension.

The online problem is harder because the user can not see all the items beforehand,
like in the offline problem. The items are presented in rounds. Thats why
the common Dinamic Programming solution does not work, and basic greedy strategies also
perform poorly.

**But the items' values and costs need to follow a known probability distribuiton, right?**
No, we assume very little about the inputs. Actually, we assume nothing about the items'
values and costs, except that the instants are presented in a random order, and that items' values
and costs are between 0 and 1. Regarding the random order input, you can think of it like this:

#. An adversary carefully and maliciously assembles every round's items.
#. The rounds order is randomized.
#. The rounds are revealed one at a time to us.
#. On each round, we have to choose which item to pack, before moving to the next round. 

.. _Knapsack Problem: https://en.wikipedia.org/wiki/Knapsack_problem


|

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents

   install
   quickstart
   online_solver
   helper
   mwu_max
   offline_solvers
   packing_problem
   instance_generator


References
----------

.. [1] Agrawal, Shipra & Devanur, Nikhil. (2014). Fast Algorithms for Online Stochastic Convex Programming. Proceedings of the Annual ACM-SIAM Symposium on Discrete Algorithms. 2015. 10.1137/1.9781611973730.93.
