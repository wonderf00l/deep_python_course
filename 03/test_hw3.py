import unittest
from unittest.mock import Mock
from hw3 import CustomList, CustomListIterator


class TestCustomList(unittest.TestCase):
    def test_init(self):
        res = [1, 2, 3, 4, 5]
        lst = CustomList([[1], 2, '2', {3: 4}, {5}])
        self.assertEqual(res, lst._CustomList__data)

    def test_computation(self):
        a = CustomList(1, 2)
        b = CustomList(3, 4)
        c = CustomList(1, 1, 1)
        d = CustomList(1)
        lst = [1, 1]
        lst1 = [1, 1, 1]
        lst2 = [1]
        self.assertEqual(a + b, [4, 6])
        self.assertEqual(a - b, [-2, -2])

        self.assertEqual(a + c, [2, 3, 1])
        self.assertEqual(a - c, [0, 1, -1])

        self.assertEqual(c + a, [2, 3, 1])
        self.assertEqual(c - a, [0, -1, 1])

        self.assertEqual(a + lst, [2, 3])
        self.assertEqual(a - lst, [0, 1])

        self.assertEqual(lst + a, [2, 3])
        self.assertEqual(lst - a, [0, -1])

        self.assertEqual(a + lst1, [2, 3, 1])
        self.assertEqual(a - lst1, [0, 1, -1])

        self.assertEqual(lst1 + a, [2, 3, 1])
        self.assertEqual(lst1 - a, [0, -1, 1])

        self.assertEqual(lst2 + a, [2, 2])
        self.assertEqual(lst2 - a, [0, -2])

        self.assertEqual(a + lst2, [2, 2])
        self.assertEqual(a - lst2, [0, 2])

        a += b
        self.assertEqual(a, [4, 6])
        a -= b
        self.assertEqual(a, [1, 2])
        b += c
        self.assertEqual(b, [4, 5, 1])
        b -= c
        self.assertEqual(b, [3, 4])
        a += d
        self.assertEqual(a, [2, 2])
        a -= d
        self.assertEqual(a, [1, 2])

        a += lst
        self.assertEqual(a, [2, 3])
        a -= lst
        self.assertEqual(a, [1, 2])
        a += lst1
        self.assertEqual(a, [2, 3, 1])
        a -= lst1
        self.assertEqual(a, [1, 2])
        a += lst2
        self.assertEqual(a, [2, 2])
        a -= lst2
        self.assertEqual(a, [1, 2])

        a = CustomList(1, 2)
        lst += a
        self.assertEqual(lst, [2, 3])
        lst -= a
        self.assertEqual(lst, [1, 1])
        lst1 += a
        self.assertEqual(lst1, [2, 3, 1])
        lst1 -= a
        self.assertEqual(lst1, [1, 1, 1])
        lst2 += a
        self.assertEqual(lst2, [2, 2])
        lst2 -= a
        self.assertEqual(lst2, [1, 0])

    def test_comparison(self):
        pass

    def test_output(self):
        pass


if __name__ == '__main__':
    unittest.main()
