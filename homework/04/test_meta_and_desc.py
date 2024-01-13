import unittest
from unittest import mock
from unittest.mock import patch
from meta_and_desc import CustomClass
from meta_and_desc import A


class MyTestCase(unittest.TestCase):
    def test_initialization_and_attr(self):
        inst = CustomClass()
        for attr in inst.__class__.__dict__:
            if attr[:2] != '__' and attr[-2:] != '__':
                self.assertEqual(f"custom_{attr[len('custom_'):]}", attr)
        inst.attr = 10
        self.assertTrue('custom_attr' in inst.__dict__)
        with self.assertRaises(AttributeError):
            print(inst.attr)

    def test_meta_edit(self):
        inst = CustomClass()
        self.assertTrue(inst.custom_x == 50)
        self.assertTrue(inst.custom_val == 99)
        self.assertTrue(inst.custom_line() == 100)
        self.assertTrue(CustomClass.custom_x == 50)
        self.assertTrue(str(inst) == "Custom_by_metaclass")

        inst.dynamic = "added later"
        self.assertTrue(inst.custom_dynamic == "added later")

        with self.assertRaises(AttributeError):
            inst.dynamic  # catches only the first exception, process separately
        with self.assertRaises(AttributeError):
            inst.x
        with self.assertRaises(AttributeError):
            inst.val
        with self.assertRaises(AttributeError):
            inst.line()
        with self.assertRaises(AttributeError):
            inst.yyy
        with self.assertRaises(AttributeError):
            CustomClass.x

    def test_descriptor_edit(self):
        inst = A(-50, "Tom", 100)
        with patch("meta_and_desc.print") as mock_print:
            self.assertEqual(inst.num, -50)
            self.assertEqual(inst.name, "TomTom")
            self.assertEqual(inst.price, 100)
            self.assertEqual(
                [
                    mock.call('even:', end=' '),
                    mock.call('short str:', end=' '),
                    mock.call('even positive:', end=' ')
                ],
                mock_print.mock_calls
            )

        with patch("meta_and_desc.print") as mock_print:
            inst.num = 155
            self.assertEqual(inst.num, 155)
            inst.name = "very_long_name"
            self.assertEqual(inst.name, "Very_long_nameVery_long_name")
            inst.price = 205
            self.assertEqual(inst.price, 205)
            self.assertEqual(
                [
                    mock.call('uneven:', end=' '),
                    mock.call('long str:', end=' '),
                    mock.call('uneven positive:', end=' ')
                ],
                mock_print.mock_calls
            )

        with self.assertRaises(AttributeError):
            inst.num = "5"
        with self.assertRaises(AttributeError):
            inst.name = 2
        with self.assertRaises(AttributeError):
            inst.price = -5


if __name__ == '__main__':
    unittest.main()
