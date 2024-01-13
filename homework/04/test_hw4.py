import unittest
from unittest import mock
from unittest.mock import patch
from hw4 import CustomClass


class MyTestCase(unittest.TestCase):
    def test_initialization_and_attr(self):
        inst = CustomClass(-3, 'name', 55)
        for attr in inst.__class__.__dict__:
            if attr[:2] != '__' and attr[-2:] != '__':
                self.assertEqual(f"custom_{attr[len('custom_'):]}", attr)
        inst.attr = 10
        self.assertTrue('custom_attr' in inst.__dict__)
        with self.assertRaises(AttributeError):
            print(inst.attr)

    def test_descriptors_valid(self):
        inst = CustomClass(-3, 'name', 55)
        with patch('hw4.print') as mock_print:
            self.assertEqual(inst.custom_num, -3)
            self.assertEqual(inst.custom_name, 'NameName')
            self.assertEqual(inst.custom_price, 55)
            self.assertEqual(
                [
                    mock.call('uneven:', end=' '),
                    mock.call('short str:', end=' '),
                    mock.call('uneven positive:', end=' ')
                ],
                mock_print.mock_calls
            )

    def test_descriptors_invalid(self):
        inst = CustomClass(-3, 'name', 55)
        with self.assertRaises(AttributeError):
            inst.num = 'w'
        with self.assertRaises(AttributeError):
            inst.name = 1
        with self.assertRaises(AttributeError):
            inst.price = -2


if __name__ == '__main__':
    unittest.main()
