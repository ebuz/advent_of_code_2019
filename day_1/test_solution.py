import unittest

from Solution import calculate_module_fuel, calculate_module_fuel_with_fuel_adjust, calculate_total_module_fuel, calculate_total_module_fuel_adjusted

class TestSolution(unittest.TestCase):

    def test_module_fuel_example1(self):
        self.assertEqual(calculate_module_fuel(12), 2)

    def test_module_fuel_example2(self):
        self.assertEqual(calculate_module_fuel(14), 2)

    def test_module_fuel_example3(self):
        self.assertEqual(calculate_module_fuel(1969), 654)

    def test_module_fuel_example4(self):
        self.assertEqual(calculate_module_fuel(100756), 33583)

    def test_total_module_fuel_example1(self):
        input_string = '12\n14\n1969\n100756'
        result = sum([2, 2, 654, 33583])
        self.assertEqual(calculate_total_module_fuel(input_string), result)

    def test_module_fuel_adjusted_example1(self):
        self.assertEqual(calculate_module_fuel_with_fuel_adjust(14), 2)

    def test_module_fuel_adjusted_example2(self):
        self.assertEqual(calculate_module_fuel_with_fuel_adjust(1969), 966)

    def test_module_fuel_adjusted_example3(self):
        self.assertEqual(calculate_module_fuel_with_fuel_adjust(100756), 50346)

    def test_total_module_fuel_adjusted_example1(self):
        input_string = '12\n1969\n100756'
        result = sum([2, 966, 50346])
        self.assertEqual(calculate_total_module_fuel_adjusted(input_string), result)

if __name__ == '__main__':
    unittest.main(verbosity = 2)
