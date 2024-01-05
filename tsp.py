from random import shuffle
from typing import List


class TSP:
    def __init__(self, nodes: List[str], weights: List[List[int]]) -> None:
        self.nodes = nodes
        self.weights = weights
        self.length = len(nodes)
        self.start = 0
        self.cost_function_cache = dict()

    def cost_function(self, walk: List[int]):
        check = tuple(walk)
        if check in self.cost_function_cache:
            return self.cost_function_cache[check]
        else:
            added_zero = list(walk)
            added_zero += [0]
            # self.length is previous length before adding 0
            val = sum(
                [
                    self.weights[added_zero[s]][added_zero[s + 1]]
                    for s in range(self.length)
                ]
            )
            self.cost_function_cache[tuple(walk)] = val
            return val

    def random_walk(self, start: int, other_locations: List[int]) -> List[int]:
        walk = [start]
        shuffle(other_locations)
        walk += other_locations
        return walk

    def get_neighbours(self, walk: List[int]):
        all_neighbours = [
            walk[: i + 1] + walk[j:] + walk[i + 1 : j]
            for i in range(self.length - 2)
            for j in range(i + 2, self.length)
        ]
        return all_neighbours

    def index_to_node(self, index: List[int]):
        new_index = list(index)
        new_index += [0]
        return " -> ".join([self.nodes[i] for i in new_index])

    def solve(self):
        other_locations = list(range(1, self.length))
        current_path = self.random_walk(start=0, other_locations=other_locations)
        lower_cost = self.cost_function(current_path)
        current_is_changed = True

        while current_is_changed == True:
            current_is_changed = False
            new_lower = 0
            associated_path = []

            all_neighbours = self.get_neighbours(current_path)
            for n in all_neighbours:
                cost = self.cost_function(n)
                if cost < lower_cost:
                    associated_path = n
                    new_lower = cost

            if new_lower != 0:
                lower_cost = new_lower
                current_path = associated_path
                current_is_changed = True

        return lower_cost, current_path
