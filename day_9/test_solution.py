import unittest

from Solution import evolve_state, run_to_halt, parse_parameter_modes

class TestSolution(unittest.TestCase):

    def test_parse_parameter_modes(self):
        inputs = ['1', '01', '001', '0001', '00001', '101', '1001', '10001', '3', '03', '103', '203']
        outputs = [['0','0','0'], ['0','0','0'], ['0','0','0'],
                ['0','0','0'], ['0','0','0'],
                ['1','0','0'], ['0','1','0'], ['0','0','1'], ['0'], ['0'], ['1'], ['2']]
        assert len(inputs) == len(outputs)
        for j,i in enumerate(inputs):
            self.assertEqual(parse_parameter_modes(i), outputs[j])

    def test_interpret_parameter_relative(self):
        inputs = [('3,2,0', 0, 0, ['5'], []), ('203,2,0', 0, 0, ['5'], [])]
        outputs = [(['3', '2', '5'], 2, 0, [], []), (['203', '2', '5'], 2, 0, [], [])]
        for j,i in enumerate(inputs):
            next_state = evolve_state(i)
            for k,f in enumerate(next_state):
                self.assertEqual(f, outputs[j][k])

    def test_evolve_state(self):
        inputs = ['00001,0,0,0,99', '02,3,0,3,99', '00002,4,4,5,99,0',
                '1101,100,-1,4,0', '1002,4,3,4,33']
        outputs = ['2,0,0,0,99', '02,3,0,6,99', '00002,4,4,5,99,9801', '1101,100,-1,4,99', '1002,4,3,4,99']
        for j,i in enumerate(inputs):
            next_state = evolve_state((i.split(','), 0, 0, [], []))
            self.assertEqual(','.join([str(i) for i in next_state[0]]), outputs[j])

    def test_inputs_outputs(self):
        inputs = [('3,2,0', 0, 0, ['5'], []), ('4,2,5', 0, 0, [], []), ('104,2,5', 0, 0, [], [])
                ]
        outputs = [(['3', '2', '5'], 2, 0, [], []), (['4', '2', '5'], 2, 0, [], ['5']), (['104', '2', '5'], 2, 0, [], ['2'])]
        for j,i in enumerate(inputs):
            next_state = evolve_state(i)
            for k,f in enumerate(next_state):
                self.assertEqual(f, outputs[j][k])

    def test_terminal_state(self):
        inputs = ['00001,0,0,0,99', '02,3,0,3,99', '00002,4,4,5,99,0']
        outputs = ['2,0,0,0,99', '02,3,0,6,99', '00002,4,4,5,99,9801']
        for j,i in enumerate(inputs):
            self.assertEqual(','.join([str(i) for i in run_to_halt(i)[0]]), outputs[j])

    def test_inputs_outputs_part2(self):
        inputs = [('3,9,8,9,10,9,4,9,99,-1,8', 0, 0, ['5'], []),
                ('3,9,8,9,10,9,4,9,99,-1,8', 0, 0, ['8'], []),
                ('3,9,8,9,10,9,4,9,99,-1,8', 0, 0, ['9'], []),
                ('3,9,7,9,10,9,4,9,99,-1,8', 0, 0, ['5'], []),
                ('3,9,7,9,10,9,4,9,99,-1,8', 0, 0, ['8'], []),
                ('3,9,7,9,10,9,4,9,99,-1,8', 0, 0, ['9'], []),
                ('3,3,1108,-1,8,3,4,3,99', 0, 0, ['5'], []),
                ('3,3,1108,-1,8,3,4,3,99', 0, 0, ['8'], []),
                ('3,3,1108,-1,8,3,4,3,99', 0, 0, ['9'], [])
                ]
        outputs = [['0'], ['1'], ['0'],
            ['1'], ['0'], ['0'],
            ['0'], ['1'], ['0']
                ]
        for j,i in enumerate(inputs):
            self.assertEqual(run_to_halt(i)[4], outputs[j], f'case: {j}')

    def test_jumps(self):
        inputs = [('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', 0, 0, ['0'], []),
                ('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', 0, 0, ['1'], []),
                ('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', 0, 0, ['0'], []),
                ('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', 0, 0, ['1'], [])
                ]
        outputs = [['0'], ['1'], ['0'], ['1']
                ]
        for j,i in enumerate(inputs):
            self.assertEqual(run_to_halt(i)[4], outputs[j])

    def test_full_computer(self):
        inputs = [('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99', 0, 0, [], []),
                ('1102,34915192,34915192,7,4,7,99,0', 0, 0, [], []),
                ('104,1125899906842624,99', 0, 0, [], [])
                ]
        outputs = ['109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'.split(','),
                [str(34915192 * 34915192)], ['1125899906842624']
                ]
        for j,i in enumerate(inputs):
            self.assertEqual(run_to_halt(i)[4], outputs[j])

if __name__ == '__main__':
    unittest.main(verbosity = 2)
