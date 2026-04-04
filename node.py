"""
node.py
Node class.
"""

class Node:
    def __init__(self, nodeId):
        self.id = nodeId # Node ID.
        self.inEdges = set() # All incoming neighbour edges.
        self.outEdges = set() # All outgoing neighbour edges.
        self.messages = [] # List of received values from incoming neighbours.
        self.replies = [] # Yes, No.
        self.type = None
    
    """
    updateType(self)
    Checks the number of incoming and outgoing edges the node has and updates type.
    If they have incoming and outgoing, they are internal.
    If they only have incoming, they are a sink.
    If they only have outgoin, they are a source.
    """
    def updateType(self):
        indeg = len(self.inEdges)
        outdeg = len(self.outEdges)

        if indeg == 0 and outdeg > 0:
            self.type = 'source'
        elif outdeg == 0 and indeg > 0:
            self.type = 'sink'
        else:
            self.type = 'internal'