#!/usr/bin/python3
"""A module for reading from a SDS011 sensor."""

import datetime
import sds011_read
import unittest
from unittest import mock


class Sds011Test(unittest.TestCase):

  def setUp(self):
    self.single_read = mock.MagicMock()
    sds011_read.single_read = self.single_read

  def test_median_read(self):
    self.single_read.side_effect = [
        (500, 100), (3, 200), (6, 50), (-1, -1), (1, 1), (7, 18), (2, 7)
    ]
    pm25, pm10 = sds011_read.median_read('ignore', reads=7, delay=0)
    self.assertEqual(pm25, 3)
    self.assertEqual(pm10, 18)

  def test_outlier_read(self):
    self.single_read.side_effect = [
        (500, 100), (50, -1),(3, 200), (600, 50), (-1, -1), (7, 18), (2, 7)
    ]
    pm25, pm10 = sds011_read.outlier_read(
        'ignore', reads=3, delay=datetime.timedelta(seconds=0),
        min_value=0.0, max_value=201.0)
    self.assertEqual(pm25, 3)
    self.assertEqual(pm10, 200)

    with self.assertRaises(ValueError):
      sds011_read.outlier_read(
        'ignore', reads=1, delay=datetime.timedelta(seconds=0))


if __name__ == '__main__':
    unittest.main()
