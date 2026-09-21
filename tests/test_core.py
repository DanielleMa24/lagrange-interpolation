"""Tests for the Lagrange interpolation core module."""

import unittest

from lagrange_interpolation.core import interpolate


class TestInterpolate(unittest.TestCase):
    def test_linear_interpolation_two_points(self):
        x = [0.0, 1.0]
        y = [1.0, 3.0]
        self.assertAlmostEqual(interpolate(x, y, 0.5), 2.0)

    def test_constant_interpolation_single_point(self):
        x = [2.0]
        y = [5.0]
        self.assertAlmostEqual(interpolate(x, y, 10.0), 5.0)

    def test_quadratic_interpolation_three_points(self):
        x = [0.0, 1.0, 2.0]
        y = [1.0, 2.0, 5.0]  # y = x^2 + x + 1
        self.assertAlmostEqual(interpolate(x, y, 1.5), 3.25)

    def test_returns_list_for_iterable_query(self):
        x = [0.0, 1.0]
        y = [1.0, 3.0]
        result = interpolate(x, y, [0.0, 0.5, 1.0])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[0], 1.0)
        self.assertAlmostEqual(result[1], 2.0)
        self.assertAlmostEqual(result[2], 3.0)

    def test_query_as_tuple(self):
        x = [0.0, 2.0]
        y = [0.0, 4.0]
        result = interpolate(x, y, (1.0, 2.0))
        self.assertEqual(result, [2.0, 4.0])

    def test_empty_points_raises_value_error(self):
        with self.assertRaises(ValueError):
            interpolate([], [], 1.0)

    def test_mismatched_lengths_raises_value_error(self):
        with self.assertRaises(ValueError):
            interpolate([0.0, 1.0], [1.0], 0.5)

    def test_duplicate_x_coordinates_raise_value_error(self):
        with self.assertRaises(ValueError):
            interpolate([1.0, 1.0], [2.0, 3.0], 0.0)

    def test_invalid_x_query_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            interpolate([0.0, 1.0], [1.0, 2.0], "not a number")

    def test_invalid_point_values_raise_type_error(self):
        with self.assertRaises(TypeError):
            interpolate([0.0, "a"], [1.0, 2.0], 0.5)
        with self.assertRaises(TypeError):
            interpolate([0.0, 1.0], [1.0, None], 0.5)

    def test_non_sequence_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            interpolate(1.0, [1.0], 0.5)

    def test_large_x_values(self):
        x = [1000.0, 1001.0]
        y = [2000.0, 2001.0]
        self.assertAlmostEqual(interpolate(x, y, 1000.5), 2000.5)


if __name__ == "__main__":
    unittest.main()
