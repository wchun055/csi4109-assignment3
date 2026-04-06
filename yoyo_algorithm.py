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
            neighbour.addMessage(source.id, source.id)

            # If a node has received messages from all their inward edges and not in processed, add to queue.
            if len(neighbour.messages) == len(neighbour.inEdges) and neighbour not in processed:
                queue.append(neighbour)
                processed.add(neighbour)

    # While there are nodes to be process, continue to process them.
    while queue:
        node = queue.popleft()
        minValue = min(node.messages.values()) # Internal nodes should only send out their minimum value.

        for neighbour in node.outEdges:
            neighbour.addMessage(node.id, minValue)
            if len(neighbour.messages) == len(neighbour.inEdges) and neighbour not in processed:
                queue.append(neighbour)
                processed.add(neighbour)

    return nodes

def yoUp(nodes):
    sinks = graph.getSinks(nodes)
    queue = deque(sinks)
    processed = set()

    for node in nodes.values(): # Clear out all past replies in a node.
        node.clearReplies()

    while queue:
        node = queue.popleft()
        processed.add(node)

        # Get minimum value from all messages.
        if node.messages:
            minVal = min(node.messages.values())
            minSenders = [sid for sid, val in node.messages.items() if val == minVal]

            for inNode in node.inEdges:
                if inNode.id in minSenders:
                    inNode.replies[node.id] = "Yes"
                else:
                    inNode.replies[node.id] = "No"

            # If all outward neighbours replied, add to processed set.
            for inNode in node.inEdges:
                allReplied = True
                
                for outNode in inNode.outEdges:
                    if outNode.id not in inNode.replies:
                        allReplied = False
                        break
                
                if allReplied and inNode not in processed and inNode not in queue:
                    queue.append(inNode)

    pruneSinks(nodes)

    pruneRedundant(nodes)

    flipEdges(nodes)

    return nodes    

"""
pruneSinks(nodes)
nodes: (Dictionary)
Prune all sink nodes that only have one incoming edge. 
Get rid of the connecting edge between the parent and the sink.
"""
def pruneSinks(nodes):
    sinks = graph.getSinks(nodes)
    
    for sink in sinks:
        if len(sink.inEdges) == 1: # Only prune sinks with one incoming edge.
            parent = next(iter(sink.inEdges)) # Get parent of the sink.
            parent.outEdges.remove(sink) # Get rid of the link from the sink and its parent.
            graph.removeNode(nodes, sink.id) # Remove sink node from node dictionary.

"""
pruneRedundant(nodes)
nodes: (Dictionary)
Prune outgoing edges with identical minimal (Yes) values.
"""
def pruneRedundant(nodes):
    for node in nodes.values():
        yEdges = []

        for nodeId, reply in node.replies.items(): # All outgoing edges with Yes reply.
            if reply == "Yes":
                yEdges.append(nodeId)

        for nodeId in yEdges[1:]: # Look at all Yes edges, skipping one.
            neighbor = None
            
            for n in node.outEdges:
                if n.id == nodeId:
                    neighbor = n
                    break # Stop if neighbour found in outgoing edges.
            
            if neighbor is not None: # If we found a neighbour, remove the connection from the edges.
                node.outEdges.remove(neighbor)
                neighbor.inEdges.remove(node)

def flipEdges(nodes):
    for node in nodes.values():
        for outNodeId, reply in node.replies.items():
            if reply == "No":
                neighbor = next((n for n in node.outEdges if n.id == outNodeId), None)
                
                if neighbor:
                    # Remove original edge.
                    node.outEdges.remove(neighbor)
                    neighbor.inEdges.remove(node)
                    
                    # Add flipped edge.
                    node.inEdges.add(neighbor)
                    neighbor.outEdges.add(node)
    
    # Update node types.
    for node in nodes.values():
        node.updateType()