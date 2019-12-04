import unittest

from Solution import is_valid, count_passwords_brute, count_passwords_range, count_passwords_range_adjusted

class TestSolution(unittest.TestCase):

    def test_is_valid(self):
        inputs = ['122345', '111123', '135679', '111111',
                '223450', '123789']
        outputs = [True, True, False, True, False, False]
        for j,i in enumerate(inputs):
            self.assertEqual(is_valid(i), outputs[j])

    def test_count_passwords(self):
        inputs = [('000000', '000022'), ('000000', '000099'),
                ('000000', '000999')]
        outputs = [20, 55, 220]
        for j,i in enumerate(inputs):
            self.assertEqual(count_passwords_brute(i[0], i[1]), outputs[j])

    def test_count_passwords(self):
        inputs = ['000000-000022', '000000-000099',
                '000000-000999']
        outputs = [20, 55, 220]
        for j,i in enumerate(inputs):
            self.assertEqual(count_passwords_range(i), outputs[j])


if __name__ == '__main__':
    unittest.main(verbosity = 2)
