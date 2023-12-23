#!/usr/bin/env python3
# Do not remove the above line, it is needed for testing

import sys

import starmap
import random
import unittest
import time

class TestStarmapMethods(unittest.TestCase):
    def test_creation(self):
        smallmap = {'Alpha_centauri': (0.0, 0.0, 0.0), 'Proxima_centauri': (0.0, 2.1, 3.2), 'Delta_Pavonis': (-3.0, 33.0, 52.0)}
        s = starmap.load_starmap("smallmap.txt")
        for item in smallmap:
            self.assertEqual(smallmap[item], s[item])
        for item in s:
            self.assertEqual(smallmap[item], s[item])

    def test_path(self):
        s = starmap.load_starmap("starmap.txt")
        reference = ["Sol", "Schrodinger", "Kumasi", "Sparta"]
        self.assertEqual(reference, starmap.traverse_starmap(s, "Sol", "Sparta", 60))
        self.assertEqual(["Sol", "Sparta"], starmap.traverse_starmap(s, "Sol", "Sparta", 300))
        self.assertEqual([], starmap.traverse_starmap(s, "Sol", "Sparta", 0.1))


    def test_comprehensive(self):
        def test_internal(star1, star2):
            print(star1, star2)
            previous = []
            shortlist = [star1, star2]
            for distance in range(0, 500, 15):
                current = starmap.traverse_starmap(s, star1, star2, distance)
                if current == []:
                    self.assertEqual(previous, [])
                else:
                    previous = current
                if previous == shortlist:
                    self.assertEqual(current, shortlist)
                else:
                    self.assertTrue(len(current) <= len(previous))
        s = starmap.load_starmap("starmap.txt")
        starlist1 = []
        starlist2 = []
        for star in s:
            starlist1.append(star)
            starlist2.append(star)
        random.shuffle(starlist1)
        random.shuffle(starlist2)
        for star1 in starlist1[:3]:
            for star2 in starlist2[:5]:
                test_internal(star1, star2)

"""Run the unit tests"""
if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass
