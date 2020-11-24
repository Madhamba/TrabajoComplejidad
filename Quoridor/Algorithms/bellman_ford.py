import networkx as nx
from collections import deque


def extraer_pesos(G, peso):
    if callable(peso):
        return peso

    if G.is_multigraph():
        return lambda u, v, d: min(attr.get(peso, 1) for attr in d.values())
    return lambda u, v, data: data.get(peso, 1)


def un_inicio_bellman_ford(G, inicio, meta=None, peso="weight"):
    if inicio == meta:
        return (0, [inicio])

    peso = extraer_pesos(G, peso)

    caminos = {inicio: [inicio]}
    dist = bellman_ford(G, [inicio], peso, caminos=caminos, meta=meta)
    if meta is None:
        return (dist, caminos)
    try:
        return (dist[meta], caminos[meta])
    except KeyError as e:
        msg = f"Node {meta} not reachable from {inicio}"
        raise nx.NetworkXNoPath(msg) from e


def bellman_ford(G, inicio, peso, padre=None, caminos=None, dist=None, meta=None, heuristic=True):
    for s in inicio:
        if s not in G:
            raise nx.NodeNotFound(f"Source {s} not in G")

    if padre is None:
        padre = {v: [] for v in inicio}

    if dist is None:
        dist = {v: 0 for v in inicio}

        # Heuristic Storage setup. Note: use None because nodes cannot be None
    nonexistent_edge = (None, None)
    pred_edge = {v: None for v in inicio}
    recent_update = {v: nonexistent_edge for v in inicio}

    G_succ = G.succ if G.is_directed() else G.adj
    inf = float("inf")
    n = len(G)

    count = {}
    q = deque(inicio)
    in_q = set(inicio)
    while q:
        u = q.popleft()
        in_q.remove(u)


        if all(pred_u not in in_q for pred_u in padre[u]):
            dist_u = dist[u]
            for v, e in G_succ[u].items():
                dist_v = dist_u + peso(u, v, e)

                if dist_v < dist.get(v, inf):
                    if heuristic:
                        if v in recent_update[u]:
                            raise nx.NetworkXUnbounded("Negative cost cycle detected.")
                        if v in pred_edge and pred_edge[v] == u:
                            recent_update[v] = recent_update[u]
                        else:
                            recent_update[v] = (u, v)

                    if v not in in_q:
                        q.append(v)
                        in_q.add(v)
                        count_v = count.get(v, 0) + 1
                        if count_v == n:
                            raise nx.NetworkXUnbounded("Negative cost cycle detected.")
                        count[v] = count_v
                    dist[v] = dist_v
                    padre[v] = [u]
                    pred_edge[v] = u

                elif dist.get(v) is not None and dist_v == dist.get(v):
                    padre[v].append(u)

    if caminos is not None:
        inicios = set(inicio)
        dsts = [meta] if meta is not None else padre
        for dst in dsts:
            gen = reconstruir_caminos_por_padres(inicios, dst, padre)
            caminos[dst] = next(gen)

    return dist


def reconstruir_caminos_por_padres(inicios, meta, padre):
    if meta not in padre:
        raise nx.NetworkXNoPath(
            f"Target {meta} cannot be reached" f"from given sources"
        )

    seen = {meta}
    stack = [[meta, 0]]
    top = 0
    while top >= 0:
        node, i = stack[top]
        if node in inicios:
            yield [p for p, n in reversed(stack[: top + 1])]
        if len(padre[node]) > i:
            stack[top][1] = i + 1
            next = padre[node][i]
            if next in seen:
                continue
            else:
                seen.add(next)
            top += 1
            if top == len(stack):
                stack.append([next, 0])
            else:
                stack[top][:] = [next, 0]
        else:
            seen.discard(node)
            top -= 1