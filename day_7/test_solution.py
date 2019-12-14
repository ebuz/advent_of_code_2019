import unittest

from Solution import evolve_state, run_to_halt, parse_parameter_modes, interpret_parameter, search_phase_sequences, loop_programs

class TestSolution(unittest.TestCase):

    def test_parse_parameter_modes(self):
        inputs = ['1', '01', '001', '0001', '00001', '101', '1001', '10001']
        outputs = [['0','0','1'], ['0','0','1'], ['0','0','1'],
                ['0','0','1'], ['0','0','1'],
                ['1','0','1'], ['0','1','1'], ['0','0','1']]
        for j,i in enumerate(inputs):
            self.assertEqual(parse_parameter_modes(i), outputs[j])

    def test_interpret_parameter(self):
        inputs = [p.split(',') for p in ['01,0,0,0,99', '101,0,0,0,99',
            '1101,0,0,0,99', '11101,0,0,0,99', '11001,0,0,0,99']]
        outputs = [['01','01','0'], ['0','101','0'],
                ['0','0','0'], ['0','0','0'], ['11001','0','0']]
        for j,i in enumerate(inputs):
            parameter_modes = parse_parameter_modes(i[0])
            parameters = [interpret_parameter(p, m, i) for p,m in zip(i[1:4], parameter_modes)]
            self.assertEqual(parameters, outputs[j])

    def test_evolve_state(self):
        inputs = ['10001,0,0,0,99', '02,3,0,3,99', '10002,4,4,5,99,0',
                '1101,100,-1,4,0', '1002,4,3,4,33']
        outputs = ['20002,0,0,0,99', '02,3,0,6,99', '10002,4,4,5,99,9801', '1101,100,-1,4,99', '1002,4,3,4,99']
        for j,i in enumerate(inputs):
            next_state = evolve_state((i.split(','), 0, [], []))
            self.assertEqual(','.join([str(i) for i in next_state[0]]), outputs[j])

    def test_inputs_outputs(self):
        inputs = [('3,2,0', 0, ['5'], []), ('4,2,5', 0, [], []), ('104,2,5', 0, [], [])
                ]
        outputs = [(['3', '2', '5'], 2, [], []), (['4', '2', '5'], 2, [], ['5']), (['104', '2', '5'], 2, [], ['2'])]
        for j,i in enumerate(inputs):
            next_state = evolve_state(i)
            for k,f in enumerate(next_state):
                self.assertEqual(f, outputs[j][k])

    def test_terminal_state(self):
        inputs = ['10001,0,0,0,99', '02,3,0,3,99', '10002,4,4,5,99,0']
        outputs = ['20002,0,0,0,99', '02,3,0,6,99', '10002,4,4,5,99,9801']
        for j,i in enumerate(inputs):
            self.assertEqual(','.join([str(i) for i in run_to_halt(i)[0]]), outputs[j])

    def test_inputs_outputs_part2(self):
        inputs = [('3,9,8,9,10,9,4,9,99,-1,8', 0, ['5'], []),
                ('3,9,8,9,10,9,4,9,99,-1,8', 0, ['8'], []),
                ('3,9,8,9,10,9,4,9,99,-1,8', 0, ['9'], []),
                ('3,9,7,9,10,9,4,9,99,-1,8', 0, ['5'], []),
                ('3,9,7,9,10,9,4,9,99,-1,8', 0, ['8'], []),
                ('3,9,7,9,10,9,4,9,99,-1,8', 0, ['9'], []),
                ('3,3,1108,-1,8,3,4,3,99', 0, ['5'], []),
                ('3,3,1108,-1,8,3,4,3,99', 0, ['8'], []),
                ('3,3,1108,-1,8,3,4,3,99', 0, ['9'], [])
                ]
        outputs = [['0'], ['1'], ['0'],
            ['1'], ['0'], ['0'],
            ['0'], ['1'], ['0']
                ]
        for j,i in enumerate(inputs):
            self.assertEqual(run_to_halt(i)[3], outputs[j])

    def test_jumps(self):
        inputs = [('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', 0, ['0'], []),
                ('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', 0, ['1'], []),
                ('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', 0, ['0'], []),
                ('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', 0, ['1'], [])
                ]
        outputs = [['0'], ['1'], ['0'], ['1']
                ]
        for j,i in enumerate(inputs):
            self.assertEqual(run_to_halt(i)[3], outputs[j])

    def test_phase_search(self):
        inputs = ['3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0',
                '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0']
        outputs = ['43210', '54321', '65210']
        for j,i in enumerate(inputs):
            self.assertEqual(search_phase_sequences(i), outputs[j])

    def test_loop(self):
        inputs = ['3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5']
        outputs = ['139629729']
        for j,i in enumerate(inputs):
            self.assertEqual(loop_programs(i), outputs[j])

if __name__ == '__main__':
    unittest.main(verbosity = 2)
