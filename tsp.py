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

    def get_nxt_lower(self, walk: Tuple[int, ...]):
        # 2-opt strategy, used chatgpt to understand definition of 2-opt
        # which is taking any two non adjacent edges and swapping them
        # swap them such that, [i, i+1] and [j, j+1] the edge between them is swapped such that
        # [i, j] and [i+1, j+1]
        current_path = tuple()
        changed = False
        current_delta_cost = 0
        current_cost = 0

        for i in range(self.length - 1):
            max_combine = self.length - 3
            if self.length - (i + 2) < max_combine:
                max_combine = self.length
            else:
                max_combine = (i + 2) + max_combine

            for j in range(i + 2, max_combine):
                self.amount_of_neighbour_checked += 1
                # inspired by https://en.wikipedia.org/wiki/2-opt#efficient-implementation
                other_end_i = (i + 1) % self.length
                other_end_j = (j + 1) % self.length
                delta_cost = (
                    self.weights[walk[i]][walk[j]]
                    + self.weights[walk[other_end_i]][walk[other_end_j]]
                ) - (
                    self.weights[walk[i]][walk[other_end_i]]
                    + self.weights[walk[j]][walk[other_end_j]]
                )

                if delta_cost < 0 and delta_cost < current_delta_cost:
                    current_path = (
                        walk[: i + 1]
                        + (walk[j],)
                        + tuple(reversed(walk[i + 1 : j]))
                        + walk[j + 1 :]
                    )
                    current_delta_cost = delta_cost
                    changed = True

        if changed == True:
            current_cost = self.cost_function(current_path)

        return current_path, current_cost, changed

    def hill_climb(self):
        current_path = self.random_walk(
            start=0, other_locations=list(range(1, self.length))
        )
        lower_cost = 0
        current_is_changed = True
        self.amount_of_neighbour_checked += 1

        while current_is_changed == True:
            current_is_changed = False
            new_path, new_lower, changed = self.get_nxt_lower(current_path)

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
