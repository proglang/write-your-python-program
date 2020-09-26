import unittest
from writeYourProgram import *

# A point has a
# - x (float)
# - y (float)
Point = Record("Point", "x", Float, "y", Float)

# Point.make: (float, float) ->  Point
# Point.isSome: any -> boolean
# Point.x: (Point) -> float
# Point.y: (Point) -> float

Square = Record("Square", "center", Point, "size", Float)

Name = Record("Name", "firstName", String, "lastName", String)

class TestRecords(unittest.TestCase):

    def test_create(self):
        p1 = Point.make(1, 2)
        p2 = Point.make(3, 4)
        self.assertEqual(Point.x(p1), 1)
        self.assertEqual(Point.y(p1), 2)
        self.assertEqual(Point.x(p2), 3)
        self.assertEqual(Point.y(p2), 4)
        square = Square.make(p1, 5)
        self.assertEqual(Square.center(square), p1)
        self.assertEqual(Square.size(square), 5)

    def test_createErrorArity(self):
        pass # FIXME

    def test_createErrorTypes(self):
        pass # FIXME

    def test_isSome(self):
        p1 = Point.make(1, 2)
        square = Square.make(p1, 5)
        self.assertTrue(Point.isSome(p1))
        self.assertFalse(Point.isSome(42))
        self.assertFalse(Point.isSome(square))
        self.assertTrue(Square.isSome(square))
        self.assertFalse(Square.isSome(42))
        self.assertFalse(Square.isSome(p1))

    def test_toString(self):
        p1 = Point.make(1, 2)
        self.assertEqual(str(p1), 'Point(x=1, y=2)')
        square = Square.make(p1, 5)
        self.assertEqual(str(square), 'Square(center=Point(x=1, y=2), size=5)')
        name = Name.make("Stefan", "Wehr")
        self.assertEqual(str(name), 'Name(firstName="Stefan", lastName="Wehr")')

    def test_eq(self):
        p1 = Point.make(1, 2)
        p2 = Point.make(1, 4)
        p3 = Point.make(1, 2)
        self.assertEqual(p1, p1)
        self.assertEqual(p1, p3)
        self.assertNotEqual(p1, p2)
        s1 = Square.make(p1, 5)
        s2 = Square.make(p3, 5)
        s3 = Square.make(p3, 6)
        s4 = Square.make(p2, 5)
        self.assertEqual(s1, s1)
        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)
        self.assertNotEqual(s1, s4)

    def test_hash(self):
        p1 = Point.make(1, 2)
        p2 = Point.make(1, 4)
        p3 = Point.make(1, 2)
        self.assertEqual(hash(p1), hash(p3))
        self.assertNotEqual(hash(p1), hash(p2))

