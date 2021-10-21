import queue
 
graf_sasiedztwa = {1: [2, 3],
                   2: [1, 5],
                   3: [4, 1],
                   4: [3, 6],
                   5: [2, 6, 8],
                   6: [4, 7, 5, 8],
                   7: [6],
                   8: [5, 6]}
 
visited = set()
q = queue.Queue()
parent = {n: None for n in graf_sasiedztwa}
start = 2
cel = 7
q.put(start)
 
while not q.empty():
    cur_n = q.get()
    ####
    ####
    ####
    if cur_n == cel:
        break
 
    for nh in graf_sasiedztwa[cur_n]:
        if nh not in visited:
            parent[nh] = cur_n
            visited.add(cur_n)
            q.put(nh) # dodajemy odwiedzanego sasiada
 
 
path = []
 
cur_n = cel
 
while cur_n != None:
    path.append(cur_n)
    cur_n = parent[cur_n]
 
reversed(path)
print(path)
