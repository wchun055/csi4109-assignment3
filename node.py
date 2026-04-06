"""
node.py
Node class.
"""

class Node:
    def __init__(self, nodeId):
        self.id = nodeId # Node ID.
        self.inEdges = set() # All incoming neighbour edges.
        self.outEdges = set() # All outgoing neighbour edges.
        self.messages = {} # Contains all retained values and who it came from. [ID]=Value
        self.replies = {} # Yes/No & the sender ID. [ID]=Yes/No
        self.type = None
    
    def updateType(self):
        indeg = len(self.inEdges)
        outdeg = len(self.outEdges)

        if indeg == 0 and outdeg > 0:
            self.type = 'source'
        elif outdeg == 0 and indeg > 0:
            self.type = 'sink'
        else:
            self.type = 'internal'

    def addMessage(self, sender, value):
        self.messages[sender] = value

    def clearMessages(self):
        self.messages.clear()

    def addReply(self, sender, value):
        self.replies[sender] = value

    def clearReplies(self):
        self.replies.clear()