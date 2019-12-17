import unittest

from Solution import setup_simulation, simulator, calculate_velocity, update_positions, update_velocities, calculate_total_energy, simulate_to_repetition, setup_sub_simulation

class TestSolution(unittest.TestCase):
    initial_inputs = ['<x=-1, y=0, z=2>\n<x=2, y=-10, z=-7>\n<x=4, y=-8, z=8>\n<x=3, y=5, z=-1>',
            '<x=-8, y=-10, z=0>\n<x=5, y=5, z=10>\n<x=2, y=-7, z=3>\n<x=9, y=-8, z=-3>'
            ]

    input1_steps = [
            [
                [[-1, 0, 2], [0, 0, 0]],
                [[2, -10, -7], [0, 0, 0]],
                [[4, -8, 8], [0, 0, 0]],
                [[3, 5, -1], [0, 0, 0]],
                ],
            [
                [[2, -1, 1], [3, -1, -1]],
                [[3, -7, -4], [1, 3, 3]],
                [[1, -7, 5], [-3, 1, -3]],
                [[2, 2, 0], [-1, -3, 1]],
                ],
            [
                [[5, -3, -1], [3, -2, -2]],
                [[1, -2, 2], [-2, 5, 6]],
                [[1, -4, -1], [0, 3, -6]],
                [[1, -4, 2], [-1, -6, 2]],
                ],
            [
                [[5, -6, -1], [0, -3, 0]],
                [[0, 0, 6], [-1, 2, 4]],
                [[2, 1, -5], [1, 5, -4]],
                [[1, -8, 2], [0, -4, 0]],
                ],
            [
                [[2, -8, 0], [-3, -2, 1]],
                [[2, 1, 7], [2, 1, 1]],
                [[2, 3, -6], [0, 2, -1]],
                [[2, -9, 1], [1, -1, -1]],
                ],
            [
                [[-1, -9, 2], [-3, -1, 2]],
                [[4, 1, 5], [2, 0, -2]],
                [[2, 2, -4], [0, -1, 2]],
                [[3, -7, -1], [1, 2, -2]],
                ],
            [
                [[-1, -7, 3], [0, 2, 1]],
                [[3, 0, 0], [-1, -1, -5]],
                [[3, -2, 1], [1, -4, 5]],
                [[3, -4, -2], [0, 3, -1]],
                ],
            [
                [[2, -2, 1], [3, 5, -2]],
                [[1, -4, -4], [-2, -4, -4]],
                [[3, -7, 5], [0, -5, 4]],
                [[2, 0, 0], [-1, 4, 2]],
                ],
            [
                [[5, 2, -2], [3, 4, -3]],
                [[2, -7, -5], [1, -3, -1]],
                [[0, -9, 6], [-3, -2, 1]],
                [[1, 1, 3], [-1, 1, 3]],
                ],
            [
                [[5, 3, -4], [0, 1, -2]],
                [[2, -9, -3], [0, -2, 2]],
                [[0, -8, 4], [0, 1, -2]],
                [[1, 1, 5], [0, 0, 2]],
                ],
            [
                [[2, 1, -3], [-3, -2, 1]],
                [[1, -8, 0], [-1, 1, 3]],
                [[3, -6, 1], [3, 2, -3]],
                [[2, 0, 4], [1, -1, -1]],
                ]
            ]

    def test_setup_simulation(self):
        outputs = [
                [
                    [[-1, 0, 2], [0, 0, 0]],
                    [[2, -10, -7], [0, 0, 0]],
                    [[4, -8, 8], [0, 0, 0]],
                    [[3, 5, -1], [0, 0, 0]]
                    ],
                [
                    [[-8, -10, 0], [0, 0, 0]],
                    [[5, 5, 10], [0, 0, 0]],
                    [[2, -7, 3], [0, 0, 0]],
                    [[9, -8, -3], [0, 0, 0]]
                    ],
                ]
        for j,i in enumerate(self.initial_inputs):
            self.assertEqual(setup_simulation(i), outputs[j])

    def test_simulator(self):
        simulation = simulator(setup_simulation(self.initial_inputs[0]))
        for i in range(len(self.input1_steps)):
            self.assertEqual(next(simulation), self.input1_steps[i])

    def test_sub_simulator(self):
        simulation = simulator(setup_sub_simulation(self.initial_inputs[0]))
        for i in range(len(self.input1_steps)):
            self.assertEqual(next(simulation), [[[m[0][0]], [m[1][0]]] for m in self.input1_steps[i]])

    def test_calculate_velocity(self):
        self.assertEqual(calculate_velocity(1, 1), 0)
        self.assertEqual(calculate_velocity(1, -1), -1)
        self.assertEqual(calculate_velocity(-1, 1), 1)

    def test_update_position(self):
        inputs_outputs = [
                [ [
                    [[-1, 0, 2], [0, 0, 0]],
                    [[2, -10, -7], [0, 0, 0]],
                    [[4, -8, 8], [0, 0, 0]],
                    [[3, 5, -1], [0, 0, 0]]
                    ],
                [
                    [[-1, 0, 2], [0, 0, 0]],
                    [[2, -10, -7], [0, 0, 0]],
                    [[4, -8, 8], [0, 0, 0]],
                    [[3, 5, -1], [0, 0, 0]]
                    ],
                ],
                [ [
                    [[-1, 0, 2], [3, -1, -1]],
                    [[2, -10, -7], [1, 3, 3]],
                    [[4, -8, 8], [-3, 1, -3]],
                    [[3, 5, -1], [-1, -3, 1]]
                    ],
                [
                    [[2, -1, 1], [3, -1, -1]],
                    [[3, -7, -4], [1, 3, 3]],
                    [[1, -7, 5], [-3, 1, -3]],
                    [[2, 2, 0], [-1, -3, 1]]
                    ],
                ],
                ]
        self.assertEqual(update_positions(inputs_outputs[0][0]), inputs_outputs[0][1])
        self.assertEqual(update_positions(inputs_outputs[1][0]), inputs_outputs[1][1])

    def test_update_velocities(self):
        inputs_outputs = [
                [ [
                    [[-1, 0, 2], [0, 0, 0]],
                    [[2, -10, -7], [0, 0, 0]],
                    [[4, -8, 8], [0, 0, 0]],
                    [[3, 5, -1], [0, 0, 0]]
                    ],
                [
                    [[-1, 0, 2], [3, -1, -1]],
                    [[2, -10, -7], [1, 3, 3]],
                    [[4, -8, 8], [-3, 1, -3]],
                    [[3, 5, -1], [-1, -3, 1]]
                    ],
                ],
                ]
        self.assertEqual(update_velocities(inputs_outputs[0][0]), inputs_outputs[0][1])

    def test_calculate_total_energy(self):
        self.assertEqual(calculate_total_energy(self.input1_steps[-1]), 179)

    def test_second_input(self):
        simulation = simulator(setup_simulation(self.initial_inputs[1]))
        for i in range(101):
            bodies = next(simulation)
        self.assertEqual(calculate_total_energy(bodies), 1940)

    def test_check_history(self):
        steps = simulate_to_repetition(self.initial_inputs[1])
        self.assertEqual(steps, 4686774924)


if __name__ == '__main__':
    unittest.main(verbosity = 2)


