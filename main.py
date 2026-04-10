# main.py
import math
import pandas as pd
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

def runTests():
    results1 = []
    messageCount = 0
    totalMessageCount = 0
    n_values = [20, 30, 40, 60, 80, 100]

    print("Beginning procedure 1...\n")

    for n in n_values:
        print("\nWorking on: n =", n)
        m_values = [n, (n * math.log2(n)), (n * math.sqrt(n)), ((n*(n-1))/2)]
        for m in m_values:
            print("m =", m)
            totalMessageCount = 0

            for i in range(1000):
                messageCount = 0

                G1 = createGraph(n, m)
                nodes1 = assignNodes(G1)
                nodes1 = convertGraphDAG(G1, nodes1)
                updateAll(nodes1)

                messageCount = 2*m

                # Continue calling yoDown() and yoUp() until we are left with one node.
                while len(nodes1) > 1:
                    nodes1, messageCount = yoDown(nodes1, messageCount)
                    nodes1, messageCount = yoUp(nodes1, messageCount)

                totalMessageCount += messageCount

            results1.append({
            "n": n,
            "m": m,
            "Average Messages": totalMessageCount / 1000
            })
                
    df1 = pd.DataFrame(results1)
    df1.to_csv("results1.csv", index=False)
    print("Result CSV file has been created. 'results1.csv'")

    results2 = []
    messageCount = 0
    totalMessageCount = 0
    m = 0

    print("Beginning procedure 2...\n")

    for n in n_values:
        m_values = [n, 2*n, 3*n, 4*n, 5*n]
        for m in m_values:
            print("\nWorking on: n =", n)
            print("m =", m)
            totalMessageCount = 0

            for i in range(1000):
                messageCount = 0

                G2 = createGraph(n, m)
                nodes2 = assignNodes(G2)
                nodes2 = convertGraphDAG(G2, nodes2)
                updateAll(nodes2)

                messageCount = 2*m

                # Continue calling yoDown() and yoUp() until we are left with one node.
                while len(nodes2) > 1:
                    nodes2, messageCount = yoDown(nodes2, messageCount)
                    nodes2, messageCount = yoUp(nodes2, messageCount)
                totalMessageCount += messageCount

            results2.append({
            "n": n,
            "m": m,
            "Average Messages": totalMessageCount / 1000
            })
                
    df2 = pd.DataFrame(results2)
    df2.to_csv("results2.csv", index=False)
    print("Result CSV file has been created. 'results2.csv'")

def plotGraph(csv):
    print("Begin plotting graph...")
    df = pd.read_csv(csv)

    plt.figure()

    # Grouping by n value.
    for n in sorted(df["n"].unique()):
        subset = df[df["n"] == n].sort_values("m")

        plt.plot(
            subset["m"],
            subset["Average Messages"],
            marker="o",
            label=f"n={n}"
        )

    plt.xlabel("m (edges)")
    plt.ylabel("Average Message Complexity")
    plt.title("Message Complexity VS. m (All n values)")
    plt.grid(True)
    plt.legend()

    print("Graph created.")

    plt.show()

# RUN HERE
if __name__ == "__main__":
    df = runTests()
    plotGraph("results1.csv")
    plotGraph("results2.csv")