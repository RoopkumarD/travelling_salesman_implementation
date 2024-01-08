# Hill Climb with 2-opt Strategy Implemented in Python

This project showcases the implementation of a local search algorithm, hill climbing, with a 2-opt strategy to find the nearest neighbor.

## Getting Started

All the implementation is encapsulated in the `tsp.py` file within the `TSP` class.

To begin, create a list of nodes and a list of lists representing the distance between each pair of nodes:

```python
nodes = [...]
cost = [[...], ...]
```

Here, `cost[row][col]` represents the distance from the node at row to the node at col.

Next, instantiate the TSP class:

```python
tsp = TSP(nodes, cost)
```

You can then apply either the `hill_climb` or `random_restart_with_hill_climb method`:

```python
print(tsp.random_restart_with_hill_climb(10))
```

To check the number of neighbors checked during the process, you can print the following:

```python
print(tsp.amount_of_neighbour_checked)
```

This should give you insights into the efficiency of the algorithm and its exploration of the solution space.
