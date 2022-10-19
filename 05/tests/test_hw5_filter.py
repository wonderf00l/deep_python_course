import unittest
from hw5_text_filter import text_filter


class MyTestCase(unittest.TestCase):
    def test_text_filter(self):
        self.assertEqual(
            text_filter('some_text.txt', ['hello', 'роза', '123']),
            ['а Роза упала на лапу Азора', 'hEllO wd', '13 123 .']
        )
        self.assertNotEqual(
            text_filter('some_text.txt', ['hello', 'роза', '123']),
            ['qweрозаrty', '123.321', 'hello-world']
        )


if __name__ == '__main__':
    unittest.main()
