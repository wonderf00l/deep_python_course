import unittest
from unittest.mock import Mock
from hw2 import ParseJson


class TestParseJson(unittest.TestCase):

    def test_parse_json_int_input(self):
        """Тест при замене JSON объекта числом"""
        parsing = ParseJson()
        with self.assertRaises(AttributeError):
            parsing.parse_json(2, parsing.required_fields, parsing.keywords, parsing.keyword_func)
        print("The end of the 'int_input' test")
        print('\n' * 2)

    def test_parse_json(self):
        """Тест алгоритма функции, проверка вызова keyword_func,
        обработка исключения в случае, если ни одно из требуемых значений
        не соответствует какому-либо из требуемых полей"""
        parsing = ParseJson()
        parsing.keyword_func = Mock()
        parsing()
        try:
            parsing.keyword_func.assert_called()
        except AssertionError:
            print("Parsing result: empty dict")
            parsing.keyword_func.assert_not_called()
        print("The end of the 'parse_json' test")
        print('\n' * 2)

    def test_keyword_func(self):
        """Тест алгоритма функции keyword_func"""
        parsing = ParseJson()
        parsing.data = '''{
                    "key1": "value1",
                    "key2": "value2",
                    "key3": 3,
                    "key4": "qq value4 q ew ",
                    "key5": "value4"
                    }'''
        parsing.required_fields = ['key1', 'key3', 'key4', 'key5']
        parsing.keywords = ['value2', 'value4']
        parsing()
        print("The end of the 'keyword_func' test")
        print('\n' * 2)
        self.assertEqual(parsing.info_dict, {'value4': 2})


if __name__ == "__main__":
    unittest.main()
