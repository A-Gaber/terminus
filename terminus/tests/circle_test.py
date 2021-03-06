"""
Copyright (C) 2017 Open Source Robotics Foundation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest
from custom_assertions_mixin import CustomAssertionsMixin
import math
from geometry.point import Point
from geometry.circle import Circle


class CircleTest(CustomAssertionsMixin, unittest.TestCase):

    def test_intersection_at_one_point_with_not_nested_circles(self):
        circle1 = Circle(Point(0, 0), 2)
        circle2 = Circle(Point(3, 0), 1)
        self.assertEqual(circle1.intersection(circle2), [Point(2, 0)])
        circle1 = Circle(Point(0, 0), 2)
        circle2 = Circle(Point(0, 3), 1)
        self.assertEqual(circle1.intersection(circle2), [Point(0, 2)])

    def test_intersection_at_one_point_in_nested_circles(self):
        circle1 = Circle(Point(0, 0), 4)
        circle2 = Circle(Point(2, 0), 2)
        self.assertEqual(circle1.intersection(circle2), [Point(4, 0)])
        circle1 = Circle(Point(0, 0), 4)
        circle2 = Circle(Point(0, 2), 2)
        self.assertEqual(circle1.intersection(circle2), [Point(0, 4)])

    def test_intersection_at_two_points(self):
        # with circles with centers at different x and different y
        circle1 = Circle(Point(0, 0), 1)
        circle2 = Circle(Point(1, 1), 1)
        self.assertEqual(circle1.intersection(circle2), [Point(1, 0), Point(0, 1)])
        # with each center outside the other circle
        circle1 = Circle(Point(-3, 0), 5)
        circle2 = Circle(Point(3, 0), 5)
        self.assertEqual(circle1.intersection(circle2), [Point(0, 4), Point(0, -4)])
        circle1 = Circle(Point(0, -3), 5)
        circle2 = Circle(Point(0, 3), 5)
        self.assertEqual(circle1.intersection(circle2), [Point(4, 0), Point(-4, 0)])
        # with each's center inside the other circle
        circle1 = Circle(Point(0, 0), math.sqrt(65))
        circle2 = Circle(Point(4, 0), 5)
        self.assertAlmostEqual(circle1.intersection(circle2), [Point(7.0, 4.0, 0.0), Point(7.0, -4.0, 0.0)])
        circle1 = Circle(Point(0, 0), math.sqrt(65))
        circle2 = Circle(Point(0, 4), 5)
        self.assertAlmostEqual(circle1.intersection(circle2), [Point(4.0, 7.0, 0.0), Point(-4.0, 7.0, 0.0)])
        # with one center inside the other circle and the line that contains both intersection points containing one circle's center
        circle1 = Circle(Point(0, 0), 5)
        circle2 = Circle(Point(-4, 0), 3)
        self.assertAlmostEqual(circle1.intersection(circle2), [Point(-4, 3), Point(-4, -3)])
        circle1 = Circle(Point(0, 0), 5)
        circle2 = Circle(Point(0, -4), 3)
        self.assertAlmostEqual(circle1.intersection(circle2), [Point(3, -4), Point(-3, -4)])
        # with each's center inside the other circle and the line that contains both intersection points separating both centers
        circle1 = Circle(Point(0, 0), 3)
        circle2 = Circle(Point(2, 0), 3)
        self.assertAlmostEqual(circle1.intersection(circle2), [Point(1, math.sqrt(8)), Point(1, -math.sqrt(8))])
        # with one center in the perimeter of the other circle
        circle1 = Circle(Point(0, 0), 1)
        circle2 = Circle(Point(1, 0), 1)
        self.assertAlmostEqual(circle1.intersection(circle2), [Point(1.0 / 2, math.sqrt(3.0 / 4)), Point(1.0 / 2, -math.sqrt(3.0 / 4))])
        circle1 = Circle(Point(0, 0), 1)
        circle2 = Circle(Point(0, 1), 1)
        self.assertAlmostEqual(circle1.intersection(circle2), [Point(math.sqrt(3.0 / 4), 1.0 / 2), Point(-math.sqrt(3.0 / 4), 1.0 / 2)])

    def test_intersection_with_circles_that_do_not_intersect(self):
        # with not nested circles
        circle1 = Circle(Point(0, 0), 2)
        circle2 = Circle(Point(6, 6), 3)
        self.assertEqual(circle1.intersection(circle2), [])
        # with nested circles
        circle3 = Circle(Point(0, 0), 4)
        circle4 = Circle(Point(2, 0), 1)
        self.assertEqual(circle3.intersection(circle4), [])

    def test_intersection_between_equal_circles(self):
        circle = Circle(Point(45, 7), 9)
        self.assertEqual(circle.intersection(circle), [circle])

    def test_intersection_with_concentric_circles(self):
        circle1 = Circle(Point(3, 3), 6)
        circle2 = Circle(Point(3, 3), 8)
        self.assertEqual(circle1.intersection(circle2), [])
