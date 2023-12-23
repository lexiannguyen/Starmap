#!/usr/bin/env python3


from graph import Graph
import math


""" A starmap file is a WELL formed file consisting of lines.  Each
line has an X, Y, and Z coordinate and then the name of the star
(which is a single word)"""



def load_starmap(f):
    """This will return a dictionary, where the key is the name of the
    star and the value is a 3-tuple for the X, Y, Z coordinate for the
    star.

    You should start by iterating over each line in the file,
    stripping out whitespace and then splitting the line into 4
    pieces, and into the resulting dictionary have the key be the
    star's name and the value being the 3-tuple of X, Y, Z
    coordinates.

    The X, Y, and Z coordinates should be floating point values.
    """
    dict = {}
    file = open(f, "r")
    for line in file:
        line = line.strip().split()
        dict[line[3]] = (float(line[0]), float(line[1]), float(line[2]))
    file.close()
    return dict


def traverse_starmap(starmap, start, end, jumpdrive):
    """In this game you have a starship that can jump between stars
    located in a 3 dimensional space up to a given distance (the
    "jumpdrive" distance)...

    So in order to go from one star to an eventual destination it will
    need to traverse a series of stars, with each star separated from
    the previous star by at most the jumpdrive distance.  In traveling
    the goal is to use the shortest path that meets these constraints.

    This will return a list that will traverse the starmap from the
    starting system to the ending system, in the shortest distance as
    long as all distances are less than or equal to the jump drive
    distance.

    Basically, create a graph for all the stars, and insert edges for
    every distance less than the jump drive distance.

    Then do a shortest path traversal and, if it finds a path to the
    destination star, report the path from the start to the
    destination inclusive. Otherwise, return the empty list.

    It should return an empty array [] if there is no path which meets
    the constraint.

    """

    myGraph = Graph(starmap)
    
    for star1 in myGraph:
        # stars connected to star1
        for star2 in myGraph:
            # if they're not the same star
            if star1 != star2:
                distance = calcDistance(star1.data, star2.data)
                
                
                # if distance between star1 and 2 is < jumpdrive
                if distance <= jumpdrive:
                    # connect star1 and star2, 
                    
                    myGraph.connect(star1.name, star2.name, distance)
    # print(myGraph)
    # return
  
    myPath = getPath(start, end, myGraph) 
        
    return myPath

def getPath(startNode, endName, graph):
    #end is a string - find node with .name == end
    hasEnd = False
    curNode = None # will be last node from dijkstras, then go backwards from here

    for node in graph.dijkstra_traversal(startNode):
        if node.name == endName:
            hasEnd = True
            curNode = node
            break
        
    if hasEnd == False:
        return [] 
    path = []

    while curNode.previous is not None:
        path.append(curNode.name)
        curNode = curNode.previous

    if curNode.name == startNode: #when it reaches the start, add it
        path.append(curNode.name)
        return list(reversed(path))
    else:
        return []
    

def calcDistance(coords1, coords2):
    # calculates the distance between 2 3D coordinates
    return math.sqrt((coords1[0] - coords2[0]) ** 2 + (coords1[1] - coords2[1]) ** 2 + (coords1[2] - coords2[2]) ** 2)



    