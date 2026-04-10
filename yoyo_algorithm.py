"""
yoyo_algorithm.py
Yo-Yo algorithm implementation.
"""

from node import Node
from collections import deque
import graph

"""
yoDown(nodes, messageCount)
nodes: (Dictionary)
messageCount: (Integer)
Sources send their ID to through out edges. Internal nodes that receive messages from all their inward 
Return updated nodes with received messages.
"""
def yoDown(nodes, messageCount):
    sources = graph.getSources(nodes) # List of sources.
    queue = deque() # Queue of nodes that have received from all of their inward edges.
    processed = set() # Nodes that have been processed from queue.

    for node in nodes.values(): # Clear out all past messages in a node.
        node.clearMessages()

    # Source nodes send their ID through their outgoing edges.
    for source in sources:
        for neighbour in source.outEdges:
            neighbour.addMessage(source.id, source.id)
            messageCount+=1

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
            messageCount+=1

            if len(neighbour.messages) == len(neighbour.inEdges) and neighbour not in processed:
                queue.append(neighbour)
                processed.add(neighbour)

    return nodes, messageCount

"""
yoUp(nodes, messageCount)
nodes: (Dictionary)
messageCount: (Integer)
Sinks send their replies, it is passed through internals and reach the sources.
Then, we prune the redundant Yes replies and sinks. We flip the edges.
"""
def yoUp(nodes, messageCount):
    sinks = graph.getSinks(nodes) # List of sinks.
    queue = deque(sinks)
    processed = set()

    for node in nodes.values():
        node.clearReplies()

    while queue:
        node = queue.popleft()

        if not node.messages:
            continue

        # Handle replies if the node is a sink.
        if node.type == "sink":
            minVal = min(node.messages.values())
            minSenders = [sid for sid, val in node.messages.items() if val == minVal]

            for inNode in node.inEdges:
                if inNode.id in minSenders:
                    inNode.replies[node.id] = "Yes"
                    messageCount+=1
                else:
                    inNode.replies[node.id] = "No"
                    messageCount+=1

        # Internal node reply.
        else:
            # Collect replies from outgoing edges.
            childReplies = [node.replies.get(out.id) for out in node.outEdges]

            if any(reply == "Yes" for reply in childReplies):
                minVal = min(node.messages.values())
                minSenders = [sid for sid, val in node.messages.items() if val == minVal]

                for inNode in node.inEdges:
                    if inNode.id in minSenders: # Only send Yes to the minimum.
                        inNode.replies[node.id] = "Yes"
                        messageCount+=1
                    else:
                        inNode.replies[node.id] = "No"
                        messageCount+=1

            # If we only have No replies, send everyone No.
            else:
                for inNode in node.inEdges:
                    inNode.replies[node.id] = "No"
                    messageCount+=1

        for inNode in node.inEdges:
            allReplied = True

            for outNode in inNode.outEdges:
                if outNode.id not in inNode.replies:
                    allReplied = False
                    break

            if allReplied and inNode not in processed and inNode not in queue:
                queue.append(inNode)

        processed.add(node) # Make sure to add nodes to processed so that we do not repeat.

    #Prune and then flip edges.
    pruneRedundant(nodes)
    pruneSinks(nodes)

    flipEdges(nodes)

    return nodes, messageCount

"""
pruneSinks(nodes)
nodes: (Dictionary)
Prune all sink nodes that only have one incoming edge. (Clean up disconnected nodes if needed.)
Get rid of the connecting edge between the parent and the sink.
"""
def pruneSinks(nodes):
    while True:
        sinks = list(graph.getSinks(nodes))
        pruned_any = False

        for sink in sinks:
            # Checking if the node is a disconnected node, and not the last node.
            if len(nodes) != 1 and (len(sink.inEdges) == 0 and len(sink.outEdges) == 0):
                graph.removeNode(nodes, sink.id-1)

            if len(sink.inEdges) == 1:
                parent = next(iter(sink.inEdges))

                parent.outEdges.discard(sink)
                sink.inEdges.discard(parent)

                graph.removeNode(nodes, sink.id-1)

                pruned_any = True # If something was pruned, we need to update all nodes and check again.

        # Skip to the end if nothing was pruned.
        if not pruned_any:
            break

        # Update nodes to check if we have new sinks (with one edge).
        updateAll(nodes)

"""
pruneRedundant(nodes)
nodes: (Dictionary)
Prune outgoing edges with identical minimal (Yes) values. (Make sure to leave one.)
"""
def pruneRedundant(nodes):
    for node in list(nodes.values()):
        yes_neighbors = []

        # Get all Yes outgoing.
        for neighbor in node.outEdges:
            if node.replies.get(neighbor.id) == "Yes":
                yes_neighbors.append(neighbor)

        # Skip if there is only one Yes.
        if len(yes_neighbors) <= 1:
            continue

        def edge_key(n):
            return node.messages.get(n.id, float('inf'))

        yes_neighbors.sort(key=edge_key)

        kept = yes_neighbors[0]

        for neighbor in yes_neighbors[1:]:
            node.outEdges.discard(neighbor)
            neighbor.inEdges.discard(node)

"""
flipEdges(nodes)
nodes: (Dictionary)
Flip edge direction that had No reply.
"""
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
    updateAll(nodes)

"""
updateAll(nodes)
nodes: (Dictionary)
Update all nodes types.
"""
def updateAll(nodes):
    for node in nodes.values():
        node.updateType()