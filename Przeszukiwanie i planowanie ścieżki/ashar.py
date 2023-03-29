import queue
import numpy as np
import math
import heapq
map = np.ones(225).reshape(15, 15)
map[1:-1, 1:-1] = 0
start = (7, 7)
end = (11, 11)
map[end] = 8
print(map)


class DFS():
    def __init__(self, start, goal, map):
        self.start = start
        self.map = map
        self.end = goal

    def down(self):
        return (0, -1)

    def up(self):
        return (0, 1)

    def left(self):
        return (-1, 0)

    def right(self):
        return (1, 0)

    def idle(self):
        return (0, 0)
    
    def find_goal(self, node):
        return node == self.end

    def is_valid(self, pose):
        return pose[1] < self.map.shape[1] and pose[0] < self.map.shape[0] and \
            pose[0] > 0 and pose[1] > 0
    
    def heuristic(self, pose):
        return abs(pose[0] - self.end[0]) + abs(pose[1] - self.end[1])
        
    def cost_to_goal(self, pose):
        return self.heuristic(pose)
    
    def cost_to_go(self, action):
        return 1.0
    
    def cost_final(self, pose, action):
        return self.heuristic(pose) + self.cost_to_go(action)

    def search(self):
        node_stack = []
        action = [self.down(), self.left(), self.up(), self.right()]
        cost_to_go = {self.start: 0}
        parent = {self.start: None}
        heapq.heappush(node_stack, (self.heuristic(self.start), (self.start)))
        while node_stack:
            # Zabierz z kolejki element ktory ma najmniejsza wartosc
            cur_penalty, cur_n = heapq.heappop(node_stack)
            # Sprawdz czy nie jest docelowym
            if self.find_goal(cur_n):
                print("goal!")
                break
            # Zaznacz jako odwiedzony
            self.map.data[cur_n] = 2
            # Oblicz sąsiada
            neighbors = [(cur_n[0] + u[0], cur_n[1] + u[1]) for u in action]
            for next_n in neighbors:
                # Dla wszystkich sasiadow nie bedacych w Q
                if self.is_valid(next_n):
                    if self.map.data[next_n] != 1:
                        go_cost = cost_to_go[cur_n] + self.cost_to_go(next_n)
                        heuristic = self.heuristic(next_n)
                        final_cost = go_cost + heuristic
                        print(f"next:= {next_n}, g():= {go_cost}, h():={heuristic}")
                        if next_n not in cost_to_go or go_cost < cost_to_go[next_n]:
                            # Oblicz final 
                            cost_to_go[next_n] = go_cost
                            parent[next_n] = cur_n
                            final_cost = go_cost + heuristic
                            heapq.heappush(node_stack, (final_cost, (next_n)))
            print(self.map)
        path = []
        cur_n = self.end
        while cur_n is not None:
            path.append(cur_n)
            cur_n = parent[cur_n]
        path.reverse()
        print(path)

A = DFS(start=start, goal=end, map=map)
A.search()
print(map)