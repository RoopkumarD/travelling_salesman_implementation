from functools import cache
from random import shuffle
from typing import List, Tuple

from profiling import profile


class TSP:
    def __init__(self, nodes: List[str], weights: List[List[int]]) -> None:
        self.nodes = nodes
        self.weights = weights
        self.length = len(nodes)
        self.start = 0
        self.amount_of_neighbour_checked = 0

    @cache
    def cost_function(self, walk: Tuple[int, ...]):
        # self.length is previous length before adding 0
        val = 0
        for s in range(self.length - 1):
            val += self.weights[walk[s]][walk[s + 1]]
        val += self.weights[walk[-1]][self.start]
        return val

    def random_walk(self, start: int, other_locations: List[int]) -> Tuple[int, ...]:
        walk = [start]
        shuffle(other_locations)
        walk += other_locations
        return tuple(walk)

    def get_nxt_lower(self, walk: Tuple[int, ...], current_cost: int):
        # 2-opt strategy, used chatgpt to understand definition of 2-opt
        # which is taking any two non adjacent edges and swapping them
        # swap them such that, [i, i+1] and [j, j+1] the edge between them is swapped such that
        # [i, j] and [i+1, j+1]
        current_path = tuple()
        changed = False

        for i in range(self.length - 1):
            max_combine = self.length - 3
            if self.length - (i + 2) < max_combine:
                max_combine = self.length - (i + 2)

            for j in range(i + 2, i + 2 + max_combine):
                self.amount_of_neighbour_checked += 1
                new_path = (
                    walk[: i + 1]
                    + (walk[j],)
                    + tuple(reversed(walk[i + 1 : j]))
                    + walk[j + 1 :]
                )
                new_cost = self.cost_function(new_path)

                if new_cost < current_cost:
                    changed = True
                    current_cost = new_cost
                    current_path = new_path

        return current_path, current_cost, changed

    def hill_climb(self):
        current_path = self.random_walk(
            start=0, other_locations=list(range(1, self.length))
        )
        lower_cost = self.cost_function(current_path)
        current_is_changed = True
        self.amount_of_neighbour_checked += 1

        while current_is_changed == True:
            current_is_changed = False
            new_path, new_lower, changed = self.get_nxt_lower(current_path, lower_cost)

            if changed == True:
                lower_cost = new_lower
                current_path = new_path
                current_is_changed = True

        return lower_cost, current_path

    @profile
    def random_restart_with_hill_climb(self, iterations: int = 10):
        lower = 1000000000000
        a = None

        for _ in range(iterations):
            c, p = self.hill_climb()
            if c < lower:
                lower = c
                a = p

        return a, lower
