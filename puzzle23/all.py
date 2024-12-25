"""
This program solves both parts of the Day 23 puzzle.
"""

from aoc import *

type clique = tuple[str, ...]
"""
The type of a clique, i.e., a collection of fully-connected nodes.
"""


class computer_graph:
    """
    Models a graph of computer connections.
    """

    connections: multidict[str, str]
    """
    Multidictionary mapping each computer to the set of computers it is
    connected. To avoid duplication, each edge a-b  is only recorded
    in the set of the node among a and b which come first in alphabetical
    order.
    """

    def __init__(self, content: list[str]):
        """
        Initialize the graph with the content of the puzzle.
        """
        self.connections = multidict()
        for line in content:
            n1, n2 = line.split("-")
            if n1 <= n2:
                self.connections.add(n1, n2)
            else:
                self.connections.add(n2, n1)

    def edges(self) -> list[tuple[str, str]]:
        """
        Return the list of edges of the graph.
        """
        return sorted(self.connections.items())

    def merge_cliques(self, l: list[clique]) -> list[clique]:
        """
        Give a list of cliques of the same size n, merge them together to get a list of cliques
        of size n+1.
        """
        result: list[clique] = []
        for i in range(len(l)):
            for j in range(i+1, len(l)):
                c1 = l[i]
                c2 = l[j]
                if c1[:-1] != c2[:-1]:
                    break
                if self.connections.check(c1[-1], c2[-1]):
                    result.append(c1 + (c2[-1], ))
        return result

    def filtered_triples(self) -> list[clique]:
        """
        Return the set of triples in which at least one node begins with "t".
        """
        edges = self.edges()
        triples = self.merge_cliques(edges)
        return [triple for triple in triples
                if any("t" in node for node in triple)]

    def lan_party(self) -> clique:
        """
        Return one of the largest clique.
        """
        newcliques = self.edges()
        oldcliques = []
        while len(newcliques) > 0:
            oldcliques = newcliques
            newcliques = self.merge_cliques(oldcliques)
        return oldcliques[0]


def main():
    content = readfile("input")
    graph = computer_graph(content)
    print("part 1:", len(graph.filtered_triples()))
    print("part 2:", ",".join(graph.lan_party()))


main()
