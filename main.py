# main.py

import networkx as nx
import matplotlib.pyplot as plt

from node import Node
from graph import createGraph, assignNodes, convertGraphDAG, getSources
from yoyo_algorithm import yoDown  # your fixed file with yoDown

################################################## TEST FUNCTIONS ##################################################
def printGraphInfo(nodes):
    for node in nodes.values():
        print(f"Node {node.id}: Type={node.type}, InEdges={[n.id for n in node.inEdges]}, "
              f"OutEdges={[n.id for n in node.outEdges]}, Messages={node.messages}")

def visualizeGraph(G, title="Graph"):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="grey", node_size=500)
    plt.title(title)
    plt.show()


if __name__ == "__main__":
    #Testing...
    #m = int(n * math.log(n))

    n = 10
    m = 15

    G = createGraph(n, m)
    visualizeGraph(G)

    nodes = assignNodes(G)

    nodes = convertGraphDAG(G, nodes)
    print("DAG Info:")
    printGraphInfo(nodes)

    yoDown(nodes)

    print()
    print("YO DOWN COMPLETE:")
    printGraphInfo(nodes)