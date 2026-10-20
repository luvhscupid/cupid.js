import unittest

import calculator


class CalculatorTests(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calculator.add(2, 3), 5)
        self.assertEqual(calculator.add(-1.5, 0.5), -1.0)

    def test_subtract(self):
        self.assertEqual(calculator.subtract(7, 4), 3)
        self.assertEqual(calculator.subtract(1.25, 2), -0.75)

    def test_multiply(self):
        self.assertEqual(calculator.multiply(6, 7), 42)
        self.assertEqual(calculator.multiply(-1.5, 2), -3.0)

    def test_divide(self):
        self.assertEqual(calculator.divide(7, 2), 3.5)
        self.assertEqual(calculator.divide(-9, 3), -3.0)

    def test_divide_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            calculator.divide(1, 0)


if __name__ == "__main__":
    unittest.main()
