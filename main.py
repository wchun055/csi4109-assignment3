# main.py

import networkx as nx
import matplotlib.pyplot as plt

from node import Node
from graph import createGraph, assignNodes, convertGraphDAG, getSources
from yoyo_algorithm import yoDown, yoUp

################################################## TEST FUNCTIONS ##################################################
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

################################################## RUN ##################################################

if __name__ == "__main__":
    n = 6
    m = 8

    G = createGraph(n, m)
    #visualizeGraph(G)

    nodes = assignNodes(G)

    nodes = convertGraphDAG(G, nodes)

    for node in nodes.values():
        node.updateType()

    #printGraphInfo(nodes)

    # Continue calling yoDown() and yoUp() until we are left with one node.
    while len(nodes) > 1:

        nodes = yoDown(nodes)
        print()
        print("YO DOWN COMPLETE:")
        printGraphInfo(nodes)

        nodes = yoUp(nodes)
        print()
        print("YO UP COMPLETE:")
        printGraphInfo(nodes)