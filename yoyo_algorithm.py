"""
yoyo_algorithm.py
Yo-Yo algorithm implementation.
"""

from node import Node
from collections import deque
import graph

"""
yoDown(nodes)
nodes: (Dictionary)
Sources send their ID to through out edges. Internal nodes that receive messages from all their inward 
Return updated nodes with received messages.
"""
def yoDown(nodes):
    sources = graph.getSources(nodes) # List of sources.
    queue = deque() # Queue of nodes that have received from all of their inward edges.
    processed = set() # Nodes that have been processed from queue.

    for node in nodes.values(): # Clear out all past messages in a node.
        node.clearMessages()

    # Source nodes send their ID through their outgoing edges.
    for source in sources:
        for neighbour in source.outEdges:
            neighbour.receiveMessage(source.id)

            # If a node has received messages from all their inward edges and not in processed, add to queue.
            if len(neighbour.messages) == len(neighbour.inEdges) and neighbour not in processed:
                queue.append(neighbour)
                processed.add(neighbour)

    # While there are nodes to be process, continue to process them.
    while queue:
        node = queue.popleft()
        minValue = min(node.messages) # Internal nodes should only send out their minimum value.

        for neighbour in node.outEdges:
            neighbour.receiveMessage(minValue)
            if len(neighbour.messages) == len(neighbour.inEdges) and neighbour not in processed:
                queue.append(neighbour)
                processed.add(neighbour)

    return nodes