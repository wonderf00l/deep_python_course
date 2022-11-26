import unittest
from file_filter import file_filter
from io import StringIO


class MyTestCase(unittest.TestCase):
    def test_text_filter(self):
        file_name = "some_text.txt"
        file_obj = StringIO(
            '''
            qweрозаrty
            123.321
            hello-world
            '''
        )
        
        for item in file_filter(file_name, ["hello", "роза", "123"]):
            self.assertTrue(
                item in [
                    "а Роза упала на лапу Азора", "hEllO wd", "13 123 ."
                ]
            )

        for item in file_filter(file_obj, ["hello", "роза", "123"]):
            self.assertTrue(
                item not in [
                    "qweрозаrty", "123.321", "hello-world"
                ]
            )


if __name__ == '__main__':
    unittest.main()
