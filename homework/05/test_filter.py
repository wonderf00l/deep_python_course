import os
import unittest
from filter import file_filter


class MyTestCase(unittest.TestCase):
    def test_filter(self):
        file_name = "test_file.txt"
        buf = []
        with open(file_name, "w+", encoding="UTF-8") as file:
            file.write("а Роза упала на лапу Азора hello 123\n"
                        "qweрозаrty\n"
                        "hello1 world\n"
                        "hEllO wd\n"
                        "123.321\n"
                        "hello-world\n"
                        "13 123 .\n"
                        "123321\n"
                        "а Роза упала на лапу Азора hello 123\n"
                        "kmr;hnglbvbФдцркгдшРФкр\n")
            file.seek(0)
            for item in file_filter(file, ["hello", "роза", "123"]):
                self.assertTrue(id(item) not in buf)
                buf.append(id(item))
                self.assertTrue(
                    item in [
                        "а Роза упала на лапу Азора hello 123", "hEllO wd", "13 123 ."
                    ]
                )
            print("End of the test for filter with f_obj arg")
            buf.clear()
        for item in file_filter(file_name, ["hello", "роза", "123"]):
            self.assertTrue(id(item) not in buf)
            buf.append(id(item))
            self.assertTrue(
                item in [
                    "а Роза упала на лапу Азора hello 123", "hEllO wd", "13 123 ."
                ]
            )
        print("End of the test for filter with str arg")
        os.remove("test_file.txt")


if __name__ == '__main__':
    unittest.main()
