import unittest

from Solution import evolve_state, run_program

class TestSolution(unittest.TestCase):

    def test_evolve_state(self):
        inputs = ['1,0,0,0,99', '2,3,0,3,99', '2,4,4,5,99,0']
        outputs = ['2,0,0,0,99', '2,3,0,6,99', '2,4,4,5,99,9801']
        for j,i in enumerate(inputs):
            self.assertEqual(','.join([str(i) for i in evolve_state(i)]), outputs[j])

    def test_terminal_state(self):
        inputs = ['1,0,0,0,99', '2,3,0,3,99', '2,4,4,5,99,0', '1,1,1,4,99,5,6,0,99']
        outputs = ['2,0,0,0,99', '2,3,0,6,99', '2,4,4,5,99,9801', '30,1,1,4,2,5,6,0,99']
        for j,i in enumerate(inputs):
            self.assertEqual(','.join([str(i) for i in run_program(i)]), outputs[j])

if __name__ == '__main__':
    unittest.main(verbosity = 2)
