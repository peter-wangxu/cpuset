import unittest

import cpuset


class CPUSetTest(unittest.TestCase):
    def setUp(self):
        self.cpuset = cpuset.CPUSet()

    def test_parse_cpuset(self):
        re = cpuset.CPUSet.Parse("0-1,3,15-19,30,21")
        self.assertEqual({0, 1, 3, 15, 16, 17, 18, 19, 21, 30}, re)
