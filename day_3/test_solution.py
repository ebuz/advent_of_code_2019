import unittest

from Solution import convert_move_to_path, nearest_cross, manhattan_distance, nearest_cross_path

class TestSolution(unittest.TestCase):

    def test_manhattan_distance(self):
        outputs = [0, 1, 1, 2, 3,
                1, 1, 2, 3, 2, 3]
        inputs = [(0,0), (1, 0), (0, 1), (1, 1), (2, 1),
                (-1, 0), (0, -1), (-1, -1), (-2, -1),
                (-1, 1), (2, -1)]
        for j,i in enumerate(inputs):
            self.assertEqual(manhattan_distance(i), outputs[j])

    def test_convert_move_to_path(self):
        inputs = ['R8,U5,L5,D3']
        outputs = [[(0,0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
            (8, 1), (8, 2), (8, 3), (8, 4), (8, 5),
            (7, 5), (6, 5), (5, 5), (4, 5), (3, 5),
            (3, 4), (3, 3), (3, 2)],]
        for j,i in enumerate(inputs):
            self.assertEqual(convert_move_to_path(i), outputs[j])

    def test_nearest_cross(self):
        inputs = ['R8,U5,L5,D3\nU7,R6,D4,L4',
                'R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83',
                'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7']
        outputs = [6, 159, 135]
        for j,i in enumerate(inputs):
            self.assertEqual(nearest_cross(i), outputs[j])

    def test_nearest_cross_path(self):
        inputs = ['R8,U5,L5,D3\nU7,R6,D4,L4',
                'R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83',
                'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7']
        outputs = [30, 610, 410]
        for j,i in enumerate(inputs):
            self.assertEqual(nearest_cross_path(i), outputs[j])

if __name__ == '__main__':
    unittest.main(verbosity = 2)
