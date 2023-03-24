import queue
import numpy as np

x = np.ones(225).reshape(15,15)
x[1:-1,1:-1] = 0
start = (7,7)
end = (11,11)
print(x)

action = [ (1, 0), (0, -1), (-1, 0), (0, 1)]

def reverse_pose( pose ):
    return (pose[1], pose[0])

# parent = {n: None for n in len(x)}
visited = set()
q = queue.LifoQueue()
q.put(start)
def main():
    while not q.empty():
        #odczytaj pierwszy wierzcholek
        cur_n = q.queue[-1]
        print("{0}".format("#"))
        print(list(q.queue), cur_n)
        print("{0}".format("#"))
        #zaznacz jako odwiedzone
        visited.add(cur_n)
        x[cur_n] = 2
        #Sprawdz czy wierzchiolek jest celem
        if cur_n == end:
            print("cel")
            break
        else:
            for u in action:
                next_n = (cur_n[0]+u[0], cur_n[1]+u[1])
                if (next_n not in visited) and x[next_n]!=1:
                    q.put(next_n)
                    break
                else:
                    if( u == action[-1]):
                        q.get()

        print(x)
    print("end")
if __name__ == "__main__":
    main()
# Dodaj wierzchołek początkowy do listy (stosu) wierzchołków do odwiedzenia
# Dopóki lista (stos) wierzchołków do odwiedzenia nie jest pusta:
# Odczytaj pierwszy wierzchołek ze stosu i zaznacz go jako odwiedzony
# Sprawdź, czy ten wierzchołek jest poszukiwanym wierzchołkiem końcowym
# Jeśli tak:  zakończ algorytm
# Jeśli nie, to sprawdź czy ten wierzchołek ma sąsiada, który nie jest odwiedzony i nie jest zajęty (nie jest ścianą)
# Jeśli tak, to dodaj tego sąsiada do stosu i idź do pkt. II.
# Jeśli nie, to usuń bieżący wierzchołek ze stosu i idź do pkt. II.