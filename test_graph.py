#!/usr/bin/env python3
# Do not remove the above line, it is needed for testing

import sys

from graph import Graph
import random
import unittest
import time

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



testdict = {"a": 1, "b": 2, "c": 3}

class TestGraphMethods(unittest.TestCase):
    def test_creation(self):
        g = Graph()

    def test_insertion(self):
        g = Graph()
        for key in testdict:
            g[key] = testdict[key]
        self.assertFalse(g.connected("a", "b"))
        g.connect("a", "b")
        self.assertTrue(g.connected("a", "b"))
        g.disconnect("a", "b")
        self.assertFalse(g.connected("a", "b"))
        
    def test_big_graph(self):
        g = Graph()
        side1 = []
        side2 = []
        for x in range(100):
            side1.append("a{}".format(x))
            side2.append("b{}".format(x))
        random.shuffle(side1)
        random.shuffle(side2)
        for e in side1:
            g[e] = "a-node"
        for e in side2:
            g[e] = "b-node"
        random.shuffle(side1)
        random.shuffle(side2)
        for e in side1:
            for e2 in side2:
                g.connect(e, e2)

        random.shuffle(side1)
        random.shuffle(side2)
        for e in side1:
            for e2 in side1:
                self.assertFalse(g.connected(e, e2))
            for e2 in side2:
                self.assertTrue(g.connected(e, e2))

        random.shuffle(side1)
        random.shuffle(side2)
        for e in side2:
            for e2 in side1:
                self.assertFalse(g.connected(e, e2))
            for e2 in side2:
                self.assertFalse(g.connected(e, e2))

        random.shuffle(side1)
        random.shuffle(side2)
        for e in side2:
            for e2 in side2:
                self.assertFalse(g.connected(e, e2))
                g.connect(e, e2)
                self.assertTrue(g.connected(e, e2))

        random.shuffle(side1)
        random.shuffle(side2)
        length = len(g)
        deleted = set()
        for delnode in side2:
            del g[delnode]
            deleted.add(delnode)
            g.check_structure()
            length += -1
            self.assertEqual(length, len(g))
            for e in side2:
                for e2 in side2:
                    if e not in deleted and e2 not in deleted:
                        self.assertTrue(g.connected(e, e2))

    def test_bft_star(self):
        legal_order = [{0}, {2, 3}, {1, 4}]
        actual_order = []
        star = make_star()
        for item in star.bfs_traversal(0):
            actual_order.append(item.name)
        for i in range(5):
            if actual_order[i] not in legal_order[(i+1)//2]:
                print("Not a valid breadth first search traversal for a star {}".format(actual_order))
                self.assertFalse(True)

    def test_linear_time(self):
        data = []
        data2 = []
        g = Graph()
        for x in range(40000):
            g[x] = "Node{}".format(x)

        reference = time.time() 
        for x in range(40000):
            self.assertFalse(g.connected(0, x))
        duration = time.time() - reference
        print("Time for 40000 connection tests with a sparse graph: {}".format(duration))
        for x in range(40000):
            g.connect(0, x)
        reference = time.time() 
        for x in range(40000):
            self.assertTrue(g.connected(0, x))
        duration2 = time.time() - reference
        print("Time for 40000 connection tests with a dense graph: {}".format(duration2))
        if duration2 > 5 * duration:
            print("connected is NOT constant time")
            self.assertFalse(True)
        
                
    def test_dft_star(self):
        star = make_star()
        actual_order = []
        legal_order = [[2, 4, 1, 3, 0], [3, 1, 4, 2, 0]]
        for item in star.dfs_traversal(0):
            actual_order.append(item.name)
        if actual_order not in legal_order:
            print("Not a valid depth first search traversal{}".format(actual_order))
            self.assertFalse(True)
        

    def test_sample_shortest(self):
        g = samplegraph()
        solution_weight = { 0:0, 1:1, 3:4, 4:5, 5:5, 2:9 }
        solution_previous = {0:None, 1:0, 3:1, 4:1, 5:0, 2:4}
        for item in g.dijkstra_traversal(0):
            assert item.distance == solution_weight[item.name]
            if item.previous != None:
                assert item.previous.name == solution_previous[item.name]
            else:
                assert item.previous == solution_previous[item.name]


"""Run the unit tests"""
if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass
