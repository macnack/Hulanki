# prob.py
# This is

import random
import numpy as np
import queue
from collections import defaultdict
import math

from gridutil import *


class Agent:
    def __init__(self, size, walls, graph, loc, dir, goal):
        self.size = size
        self.walls = walls

        # list of valid locations
        self.locations = list(graph.keys())
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir
        self.goal = goal
        self.t = 0
        graph_with_cost = defaultdict(list)
        cost = queue.Queue()
        for point_A in graph.keys():
            for point_B in graph[point_A]:
                cost.put(np.round(np.sqrt(np.power(point_B[0] - point_A[0], 2) + np.power(point_B[1] - point_A[1], 2))))
            for index in range(len(graph[point_A])):
                graph_with_cost[point_A].append((graph[point_A][index], cost.get()))
        self.graph = graph_with_cost

        self.path = self.find_path()

    def __call__(self):
        action = self.loc

        # select action to reach first location in self.path
        # TODO PUT YOUR CODE HERE

        # ------------------

        return action

    def find_path(self):
        path = []
        start = self.loc
        cel = self.goal
        q = queue.PriorityQueue()
        visited = set()
        parent = {n: None for n in self.locations}
        cost = {n: math.inf for n in self.locations}
        cost[start] = 0
        q.put((cost[start], start))
        print(self.graph)
        while not q.empty():
            _, cur_n = q.get()
            if cur_n in visited:
                continue

            visited.add(cur_n)

            if cur_n == cel:
                break
            for nh, distance in self.graph[cur_n]:
                if nh in visited:
                    continue
                old_cost = cost[nh]
                new_cost = cost[cur_n] + distance
                if new_cost < old_cost:
                    cost[nh] = new_cost
                    parent[nh] = cur_n
                    priority = new_cost + manhatDist(cel, nh)
                    q.put((priority, nh))
        path = []
        cur_n = cel
        while cur_n is not None:
            path.append(cur_n)
            cur_n = parent[cur_n]
        path.reverse()
        return path

    def get_path(self):
        return self.path
