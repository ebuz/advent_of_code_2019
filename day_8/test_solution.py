import unittest

from Solution import check_for_corruption, build_image

class TestSolution(unittest.TestCase):

    def test_check_for_corruption(self):
        inputs = ['123456789012', '122456789012', '222456789012', '123450789112']
        outputs = [1, 2, 0, 2]
        for j,i in enumerate(inputs):
            self.assertEqual(check_for_corruption(i, 3, 2), outputs[j])

    def test_build_image(self):
        inputs = [('0222112222120000', 2, 2), ('022201112222221211000011', 2, 3)]
        outputs = ['█1\n1█', '█1\n1█\n█1']
        for j,i in enumerate(inputs):
            self.assertEqual(build_image(*i), outputs[j])


if __name__ == '__main__':
    unittest.main(verbosity = 2)
