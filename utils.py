from random import shuffle
from typing import List


def random_walk(start: int, other_locations: List[int]):
    walk = "" + str(start)
    shuffle(other_locations)
    walk += "".join([str(k) for k in other_locations])
    return walk


def get_neighbours(walk: str):
    length = len(walk)
    all_neighbours = [
        walk[: i + 1] + walk[j:] + walk[i + 1 : j]
        for i in range(length - 2)
        for j in range(i + 2, length)
    ]

    return all_neighbours


if __name__ == "__main__":
    # k = random_walk(1, [2, 3, 4])
    # print(k)
    k = "1324"
    print(get_neighbours(k))
