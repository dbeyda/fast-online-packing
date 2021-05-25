Fast Online Packing Docs and API Reference
==========================================

This package aims to solve the Online Packing Problem, under the
random order model, and is an implementation of the algorithm
presented by Agrawal and Devanur [1]_.

What is an Online Packing Problem?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The Knapsack Problem.** If you are here, you probably heard of the `Knapsack Problem`_: given a set of
items (each one with it's own value and weight), choose which items to pack
in order to maximize the value that fits the backpack's weight restriction.
Notice each item has a "cost" (weight), which we have a restriction on. Also, consider
you can only pack, at maximum, one copy of each item.

**Multidimensional Costs**. Now let's get into the Multidimensional Knapsack Problem: it's the same as the above,
but the items cost is now a vector, meaning the cost has more than one dimension.
You can interpret each dimension as separate restriction. For example, we could have a cost vector of 
2 dimensions, one for the items' weights, another for the items' prices.

**What about the Online part?** A problem is called online when you have limited information about
the problem and you have to make a choice using only the little information you have. In the
future, more information will be revealed, you will be asked to make other choices, but past choices cannot be changed.

**The complete picture**. The problem develops in rounds. On each round, `k` items are presented to the
algorithm. The algorithm should pack zero or one of the presented items, before proceeding to the next round.
We have a restriction of `B` in every cost dimension (sum of packed items costs for any dimension must
be lower or equal to `B`). The objective is to maximize the packed value, without exceeding the
restriction of `B` in any dimension.

The online problem is harder because the user can not see all the items beforehand,
like in the offline problem. The items are presented in rounds. Thats why
the common Dynamic Programming approach does not work, and basic greedy strategies also
perform poorly.

**But the items' values and costs need to follow a known probability distribuiton, right?**
No, we assume very little about the inputs. Actually, we assume nothing about the items'
values and costs, except that the instants are presented in a random order, and that items' values
and costs are between 0 and 1. Regarding the random order input, you can think of it like this:

#. An adversary carefully and maliciously assembles every round's items.
#. The rounds order is randomized.
#. The rounds are revealed one at a time to us.
#. On each round, we have to pack zero or one item, before moving to the next round. 

.. _Knapsack Problem: https://en.wikipedia.org/wiki/Knapsack_problem


|

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents

   install
   quickstart
   instance_generator
   packing_problem
   helper
   mwu_max
   offline_solvers
   online_solver


References
----------

.. [1] Agrawal, Shipra & Devanur, Nikhil. (2014). Fast Algorithms for Online Stochastic Convex Programming. Proceedings of the Annual ACM-SIAM Symposium on Discrete Algorithms. 2015. 10.1137/1.9781611973730.93.
