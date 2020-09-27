

from codigo.Algoritmos.algorithms_util import para_un_vertice

# El atributo de las aristas ser[a por defecto weight
def dijkstra_camino(G, inicio, final, atributo="weight"):
    def func(u, v, d):
        node_u_wt = G.nodes[u].get("node_weight", 1)
        node_v_wt = G.nodes[v].get("node_weight", 1)
        edge_wt = d.get("weight", 1)
        return node_u_wt / 2 + node_v_wt / 2 + edge_wt

    (distancia_total, camino) = para_un_vertice(G, inicio, final=final, atributo=atributo)
    return camino