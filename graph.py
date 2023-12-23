#!/usr/bin/env python3

from collections import deque

# problem : all_edges isn't returning the graphnode object

class GraphNode():
    def __init__(self, name, data=None):
        """Initialization for the node itself.

        This is for a more efficient implementation: Instead of having
        a set of edges, this one should use a dictionary with a key
        for each destination node and the value being the weight for
        the edge.

        This will allow connected() and disconnect() to operate in
        linear time.

        Functions you need to implement in the new version will raise
        NotImplemented exceptions until you update the code.

        """

        self.data = data
        self.name = name

        # This is the new represntation of a dictionary mapping
        # nodes to edge weights
        self.edges = {}

        # We also maintain a set of backward edges from dest->source
        # so we can go backwards even though it is a directed graph.
        self.back_edges = {}

        # Parameters generated during traversals.  We initialize them
        # here for error checking purposes
        self.color = "none-set"
        self.previous = None
        self.distance = float('inf')
 

    def connect(self, dest_node, weight=1): #HW
        """Connects this node to another node.

        Important notes: It assumes a directed graph, and you need to
        connect the other way if you want an undirected graph.  It
        also does NOT allow multiple connections to the same
        destination, and enforces this with an assertion.
        """
        # given
        if self.connected(dest_node):
            raise Exception("An edge already exists")
        
        # check: dest_node is a graphnode
        if not isinstance(dest_node, GraphNode):
            raise TypeError("dest_node must be an instance of GraphNode")
        
        # connects from current to dest
        self.edges[dest_node] = weight

        # connect from dest to current
        dest_node.back_edges[self] = weight
        

    def connected(self, dest_node): 
        """A connectivity check.

        You will need to update this for the new version."""
        return dest_node in self.edges

        
    def disconnect(self, dest_node):
        if not self.connected(dest_node):
            raise Exception("No edge exists between {} and {}".format(
                self.name, dest_node))
        
        del self.edges[dest_node] #delete from current node to destination node w/ dict key

        # not sure if this is necessary ?
        if self in dest_node.back_edges: # checks to see if it was connected first
            del dest_node.back_edges[self] # delete back edge from dest to current
        # raise NotImplementedError

    def __bool__(self):
        """Needed to keep python from getting too smart because we
        may also have __len__ defined"""
        return True

    def _check_structure(self): #HW !
        """A sanity check function that makes sure that every edge is well
        formed.

        """
        # no idea what to write here
        

        for dest_node, weight in self.all_edges():
            assert weight >= 0
        print(str(self.name) + " is well formed ")

        # raise NotImplementedError
            
        
    
    def __repr__(self):
        """A sensible repr function"""
        
        return ("( {}/{} [".format(self.name, self.data) +
                ", ".join(
                    map(
                        lambda x: "{}->{}".format(x[1],
                                                  x[0].name),
                        self.all_edges()))
                + "])")

    def __str__(self):
        return "Name: {}".format(self.name)
    
    def all_edges(self):
        """This iterates over all nodes it is connected TO in
        unspecified order, returning a tuple of (destination-node,
        edge-weight)
        """
    

        for dest_node in self.edges:
            yield dest_node, self.edges[dest_node]



    def del_all_edges(self):
        """This deletes all edges TO and FROM the graph...

        An important note on dictionaries: You can NOT delete from a
        dictionary from within a loop over the dictionary.
        """

        
        for dest_node, weight in self.all_edges():
            # delete ref to self from backedges first
            if self in dest_node.back_edges:
                del dest_node.back_edges[self]

        for from_node in self.back_edges:
            if self in from_node.edges:
                del from_node.edges[self]
        
        # then delete self's edges (refs to other nodes)
        self.edges.clear()
        self.back_edges.clear() #also del self's backedges


class Graph():
    """This is effectively the graph code from the lecture.  Thanks to
    the abstractions for nodes, the code works with your new version
    as well
    """
    def __init__(self, dictionary=None):
        """Initializes a graph"""
        
        self.nodes = {}


        if dictionary:
            for key in dictionary:
                self[key] = dictionary[key] 
        
    def __getitem__(self, name):
        """This returns the NODE itself, not the data in the node.

        We do this as returning the node because there are many things
        we want to do with nodes.
        """
        if name not in self.nodes:
            raise IndexError("Unable to find {}".format(name))
        return self.nodes[name]

    def __setitem__(self, name, data):
        if name in self.nodes:
            self.nodes[name].data = data
        else:
            self.nodes[name] = GraphNode(name, data)

    def __delitem__(self, name):
        """For deleting nodes, we delete all the edges involved in a
        node first..."""
        if name not in self.nodes:
            raise IndexError("Unable to find {}".format(name))
        self.nodes[name].del_all_edges()
        del self.nodes[name]

    def __contains__(self, name):
        return name in self.nodes

    def __iter__(self):
        for name in self.nodes:
            yield self.nodes[name]
    
    def connect(self, source_name, dest_name, weight=1):
        """This will implicitly raise errors if nodes don't exist..."""
        source = self[source_name]
        dest = self[dest_name]
        source.connect(dest, weight)

    def disconnect(self, source_name, dest_name):
        source = self[source_name]
        dest = self[dest_name]
        source.disconnect(dest)
        
    def connected(self, source_name, dest_name):
        source = self[source_name]
        dest = self[dest_name]
        return source.connected(dest)
        
    def check_structure(self):
        """Will raise an assertion failure if it is not well formed"""
        for node in self.nodes:
            self.nodes[node]._check_structure()
        return True


    def dijkstra_traversal(self, node_name):
        """This traversal is the shortest path traversal starting from
        the node.

        Note that it will return all nodes, even those who are not
        reachable from the starting node, but such nodes will have no
        "previous" value."""
        start = self.nodes[node_name]
        unvisited = set()
        for n in self.nodes:
            self.nodes[n].distance = float('inf')
            self.nodes[n].previous = None
            unvisited.add(self.nodes[n])
            for (dest, weight) in self.nodes[n].all_edges():
                assert weight >= 0
        start.distance = 0
        while len(unvisited) > 0:
            min_node = None
            for node in unvisited:
                if min_node == None:
                    min_node = node
                if node.distance < min_node.distance:
                    min_node = node

            unvisited.remove(min_node)
            for (dest, weight) in min_node.all_edges():
                if ( dest in unvisited and
                     min_node.distance + weight < dest.distance):
                    dest.distance = min_node.distance + weight
                    dest.previous = min_node
            yield min_node
            
    def bfs_traversal(self, node_name):

        """Does an iterative breadth first search traversal"""
        for n in self.nodes:
            self.nodes[n].color = "white"
            self.nodes[n].previous = None
        start_node = self[node_name]
        queue = deque()
        start_node.color = "gray"
        queue.appendleft(start_node)
        while len(queue) != 0:
            node = queue.pop()
            for (dest, weight) in node.all_edges():
                if dest.color == "white":
                    dest.color = "gray"
                    dest.previous = node
                    queue.appendleft(dest)
            node.color = "black"
            yield node


    def dfs_iterative_traversal(self, node_name):
        """Does an iterative depth first search traversal"""
        for n in self.nodes:
            self.nodes[n].color = "white"
            self.nodes[n].previous = None
        start_node = self[node_name]
        queue = []
        queue.append(start_node)
        start_node.color = "gray"
        while len(queue) != 0:
            node = queue[len(queue)-1]
            appended = False
            for (dest, weight) in node.all_edges():
                if dest.color == "white":
                    dest.color = "gray"
                    dest.previous = node
                    queue.append(dest)
                    appended = True
            if not appended:
                node = queue.pop()
                node.color = "black"
                yield node
            
    def dfs_traversal(self, node_name):
        """Does a depth first search traversal recursively.  Note that
        this can sometimes blow out the python stack, so the iterative
        one is perferred in practice"""
        def dfs_internal(at):
            at.color = "gray"
            for (dest, edge) in at.all_edges():
                if dest.color == "white":
                    dest.previous = at
                    yield from dfs_internal(dest)
            at.color = "black"
            yield at
        for n in self.nodes:
            self.nodes[n].color = "white"
            self.nodes[n].previous = None
        yield from dfs_internal(self.nodes[node_name])
        
    def __len__(self):
        return len(self.nodes)

    def __repr__(self):
        
        return "{ " + ", ".join(map(lambda x: repr(self.nodes[x]),
                                    self.nodes)) + "}" 


def make_star():
    """A basic test graph of a star"""
    g = Graph()
    nums = "01234"
    for i in range(5):
        g[i] = "Node{}".format(i)
    for i in range(5):
        g.connect(i, (i+2) % 5)
        g.connect(i, (i-2) % 5)
    return g
        

def samplegraph():
    """The basic test graph used in class"""
    g = Graph()
    connections = [(0,1,1), (0,5,5),
                   (1,2,20), (1,3,3), (1,4,4),
                   (2,0,2), (3,4,4),
                   (4,2,4)]
    for i in range(6):
        g[i] = "Node{}".format(i)
    for source, dest, weight in connections:
        g.connect(source, dest, weight)
    return g


