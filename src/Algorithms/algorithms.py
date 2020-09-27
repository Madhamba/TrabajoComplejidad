import itertools as itr
import heapq as hq

from src.Algorithms.algorithms_util import para_un_vertice

# El atributo de las aristas ser[a por defecto weight
def dijkstra_camino(G, inicio, final, atributo="weight"):
    def func(u, v, d):
        node_u_wt = G.nodes[u].get("node_weight", 1)
        node_v_wt = G.nodes[v].get("node_weight", 1)
        edge_wt = d.get("weight", 1)
        return node_u_wt / 2 + node_v_wt / 2 + edge_wt

    (distancia_total, camino) = para_un_vertice(G, inicio, final=final, atributo=atributo)
    return camino

def a_star(G, nodo_inicial, nodo_final):
    push = hq.heappush
    pop = hq.heappop
    contar = itr.count()
    cola = [(0, next(contar), nodo_inicial, 0, None)]
    en_cola = {}
    explorados = {}
    while cola:
        _, __, actual, dist, padre = pop(cola)

        if actual == nodo_final:
            camino = [actual]
            nodo = padre
            while nodo is not None:
                camino.append(nodo)
                nodo = explorados[nodo]
            camino.reverse()
            return camino

        if actual in explorados:
            if explorados[actual] is None:
                continue
            qcosto, h = en_cola[actual]
            if qcosto < dist:
                continue

        explorados[actual] = padre

        for vecino, w in G[actual].items():
            ncosto = dist + 1
            if vecino in en_cola:
                qcosto, h = en_cola[vecino]
                if qcosto <= ncosto:
                    continue
            else:
                h = 0
            en_cola[vecino] = ncosto, h
            push(cola, (ncosto + h, next(contar), vecino, ncosto, actual))

    print("No existe camino entre el nodo inicial y el nodo final")