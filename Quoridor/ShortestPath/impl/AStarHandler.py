import ShortestPath.ShortestPathHandler
import networkx as nx

from Algorithms.algorithms import a_star


class AStarHandler(ShortestPath.ShortestPathHandler.ShortestPathHandle):
    def get_shortest_path(self, movable):
        winning_nodes = [n for n, d in movable.board.G.nodes(data=True) if d['is_winning_pos']]
        best_path = None
        for node in winning_nodes:
            try:
                path = a_star(movable.board.G, (movable.y, movable.x), node)
            except nx.exception.NetworkXNoPath:
                return []
            if best_path is None or len(path) < len(best_path):
                best_path = path
        if best_path:
            return best_path
        else:
            return []
