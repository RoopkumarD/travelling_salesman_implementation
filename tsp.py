from functools import cache
from random import shuffle
from typing import List, Tuple

# from profiling import profile


class TSP:
    def __init__(self, nodes: List[str], weights: List[List[int]]) -> None:
        self.nodes = nodes
        self.weights = weights
        self.length = len(nodes)
        self.amount_of_neighbour_checked = 0

    @cache
    def cost_function(self, walk: Tuple[int, ...]):
        # self.length is previous length before adding 0
        val = 0
        for s in range(self.length - 1):
            val += self.weights[walk[s]][walk[s + 1]]
        val += self.weights[walk[-1]][walk[0]]
        return val

    def random_walk(self, num_of_elem: int) -> Tuple[int, ...]:
        k = list(range(num_of_elem))
        shuffle(k)
        return tuple(k)

    def get_nxt_lower(self, walk: Tuple[int, ...]):
        # 2-opt strategy, used chatgpt to understand definition of 2-opt
        # which is taking any two non adjacent edges and swapping them
        # swap them such that, [i, i+1] and [j, j+1] the edge between them is swapped such that
        # [i, j] and [i+1, j+1]
        changed = False
        swap1, swap2 = None, None
        current_delta_cost = 0

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
                    swap1 = i
                    swap2 = j
                    current_delta_cost = delta_cost
                    changed = True

        current_path = tuple()
        if changed == True and swap1 != None and swap2 != None:
            current_path = (
                walk[: swap1 + 1]
                + (walk[swap2],)
                + tuple(reversed(walk[swap1 + 1 : swap2]))
                + walk[swap2 + 1 :]
            )

        return current_path, changed

    def hill_climb(self):
        # using 0th posn as starting point
        current_path = self.random_walk(self.length)
        current_is_changed = True
        self.amount_of_neighbour_checked += 1

        while current_is_changed == True:
            current_is_changed = False
            new_path, changed = self.get_nxt_lower(current_path)

            if changed == True:
                current_path = new_path
                current_is_changed = True

        return self.cost_function(current_path), current_path

    # @profile
    def random_restart_with_hill_climb(self, iterations: int = 10):
        lower = 1000000000000
        a = None

        for _ in range(iterations):
            c, p = self.hill_climb()
            if c < lower:
                lower = c
                a = p

        final = []
        if a != None:
            for elem in a:
                final += self.nodes[elem]

        return final, lower
