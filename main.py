# main.py
import math
import networkx as nx
import matplotlib.pyplot as plt

from node import Node
from graph import createGraph, assignNodes, convertGraphDAG, removeNode
from yoyo_algorithm import yoDown, yoUp, updateAll

"""
Test functions to print out graph + node info.
"""
def printGraphInfo(nodes):
    for node in nodes.values():
        print(f"Node {node.id}: "
              f"Type={node.type}, "
              f"InEdges={[n.id for n in node.inEdges]}, "
              f"OutEdges={[n.id for n in node.outEdges]}, "
              f"Messages={node.messages}, "
              f"Replies={node.replies}")

def visualizeGraph(G, title="Graph"):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="grey", node_size=500)
    plt.title(title)
    plt.show()

# RUN HERE
if __name__ == "__main__":
    n_values = [20, 30, 40, 60, 80, 100]

    for n in n_values:
        m_values = [n, (n * math.log2(n)), (n * math.sqrt(n)), ((n*(n-1))/2)]
        print("n: ", n)

        for m in m_values:
            print("m: ", m)

            G = createGraph(n, m)
            #visualizeGraph(G)

            nodes = assignNodes(G)

            nodes = convertGraphDAG(G, nodes)

            updateAll(nodes)

            #printGraphInfo(nodes)

            # Continue calling yoDown() and yoUp() until we are left with one node.
            while len(nodes) > 1:
                nodes = yoDown(nodes)
                nodes = yoUp(nodes)