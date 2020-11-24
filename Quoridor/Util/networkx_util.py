def get_attr_val(G, node, attribute):
    if node in G.nodes:
        return G.nodes[node][attribute]


def remove_node_util(G, node):
    if node in G.nodes:
        G.remove_node(node)


def add_node_util(G, node):
    if node not in G.nodes:
        G.add_node(node)


def remove_edge_util(G, u, v):
    if u in G.nodes and v in G.nodes:
        if (u, v) in G.edges:
            G.remove_edge(u, v)
        if (v, u) in G.edges:
            G.remove_edge(v, u)


def add_edge_util(G, u, v):
    if u in G.nodes and v in G.nodes:
        if (u, v) not in G.edges and (v, u) not in G.edges:
            G.add_edge(u, v)
