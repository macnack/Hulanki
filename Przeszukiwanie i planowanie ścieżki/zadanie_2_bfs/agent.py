# prob.py
# This is

import random
import numpy as np
import queue

from gridutil import *


class Agent:
    def __init__(self, size, walls, loc, dir, goal):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir
        self.goal = goal

        self.t = 0
        self.path = self.find_path()

    def __call__(self):
        for dir in  ['N', 'E', 'S', 'W']:
            if ( nextLoc(self.path[0], dir) == self.path[1] ):
                action = dir
        self.path = self.path[1:]


        # ------------------
        return action

    def find_path(self):
        start = self.loc
        cel = self.goal
        q = queue.Queue()
        q.put(start)
        path = []
        visited = set()
        parent = {n: None for n in self.locations}
        graph = {}
        for n in self.locations:
            nhs = []
            for dir in ['N', 'E', 'S', 'W']:
                buff = nextLoc( n, dir)
                if buff in self.locations:
                    nhs.append(buff)
            graph[n] = nhs
        while not q.empty():
            cur_n = q.get()
            if cur_n == cel:
                break

            for nh in graph[cur_n]:
                if nh not in visited:
                    parent[nh] = cur_n
                    visited.add(cur_n)
                    q.put(nh)  # dodajemy odwiedzanego sasiada
        cur_n = cel

        while cur_n != None:
            path.append(cur_n)
            cur_n = parent[cur_n]
        return path

    def get_path(self):
        return self.path
