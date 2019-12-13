import unittest

from Solution import tabulate_orbits, orbit_transfers

class TestSolution(unittest.TestCase):

    def test_tabulate(self):
        inputmap = 'COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\n'
        output = 42
        self.assertEqual(tabulate_orbits(inputmap), output)

    def test_path(self):
        inputmap = 'COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN\n'
        output = 4
        self.assertEqual(orbit_transfers(inputmap), output)

if __name__ == '__main__':
    unittest.main(verbosity = 2)



