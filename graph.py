"""
graph.py
Handles graph creation, DAG creation and node assigning.
"""

from node import Node
import math, random
import networkx as nx
import matplotlib.pyplot as plt

"""
createGraph(n, m)
n: (Integer) Number of nodes in the graph.
m: (Integer) Number of edges in the graph.
Returns G, the resulting graph created using n and m.
Creates a spanning tree, if required will add more edges to ensure it reaches the edge requirement.
"""
def createGraph(n, m):
    minEdges = n - 1
    maxEdges = n * (n - 1) // 2
    
    # Check if edges are sufficient number.
    if m < minEdges:
        raise ValueError(f"m = {m}, requries minimum of {minEdges} edges.")
    if m > maxEdges:
        raise ValueError(f"m = {m}, exceeding maximum of {maxEdges} edges.")

    G = nx.Graph()
    G.add_nodes_from(range(n))

    # Creating a spanning tree.
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(1, n):
        u = nodes[i]
        v = nodes[random.randint(0, i - 1)]
        G.add_edge(u, v)

    # Add extra edges to reach m edges.
    potentialEdges = [(i, j) for i in range(n) for j in range(i + 1, n)] # Ensure they are not repeat edges.
    random.shuffle(potentialEdges)
    for u, v in potentialEdges:
        if G.number_of_edges() >= m:
            break
        if  u != v and not G.has_edge(u, v):
            G.add_edge(u, v)

    return G

"""
assignNodes(G)
G: (nx.Graph) Graph object.
Gets number of nodes from graph G, assign each node a random, unique node ID.
Returns a dictionary of n Node objects. (No internal or outgoing edges assigned to the nodes.)
"""
def assignNodes(G):
    n = G.number_of_nodes()
    nodes = {}
    
    nodeIds = list(range(1, n + 1))

    for i, graphNode in enumerate(G.nodes()):
        node = Node(nodeId=nodeIds[i])
        nodes[graphNode] = node
        
    return nodes

"""
convertGraphDAG(G, nodes)
G: (nx.Graph) Graph object.
nodes: (Dictionary) All nodes in the graph with unique IDs.
Converts undirected graph G to a DAG. 
Iterate through all edges, then assign depending on: smaller IDs -> greater IDs.
Returns an updates dictionary of the nodes, now with assigned incoming/outgoing edges.
"""
def convertGraphDAG(G, nodes):
    # Iterate over all edges in G.
    for nodeLabelA, nodeLabelB in G.edges():
        nodeA = nodes[nodeLabelA]
        nodeB = nodes[nodeLabelB]
        
        # Determine edge direction based on ID.
        if nodeA.id < nodeB.id: # A -> B
            nodeA.outEdges.add(nodeB)
            nodeB.inEdges.add(nodeA)

        elif nodeB.id < nodeA.id: # B -> A
            nodeB.outEdges.add(nodeA)
            nodeA.inEdges.add(nodeB)

    # Nodes can check their edges and update their type.
    for node in nodes.values():
        node.updateType()

    return nodes

"""
getSources(nodes)
nodes: (Dictionary) Nodes in the DAG graph.
Checks all the nodes and retrieves the sources.
Returns a list of all source nodes.
"""
def getSources(nodes):
    sources = []
    
    for node in nodes.values():
        if node.type == 'source':
            sources.append(node)
    
    return sources

"""
getSinks(nodes)
nodes: (Dictionary) Nodes in the DAG graph.
Checks all the nodes and retrieves the sinks.
Returns a list of all sink nodes.
"""
def getSinks(nodes):
    sources = []
    
    for node in nodes.values():
        if node.type == 'sink':
            sources.append(node)
    
    return sources

def removeNode(nodes, id):
    if id in nodes:
        del nodes[id]

    return nodes