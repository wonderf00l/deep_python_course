import unittest
from unittest import mock

from user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.guido = User("Guido", 50)

    def test_greetings_bad(self):
        user = User("", 10)
        self.assertEqual(user.greetings(), "Hello, !")

    def test_greetings(self):
        self.assertEqual(self.guido.greetings(), "Hello, Guido!")
        self.assertNotEqual(self.guido.greetings(), "Hello, Van!")

    def test_birthday(self):
        self.assertEqual(50, self.guido.age)
        self.assertEqual(51, self.guido.birthday())
        self.assertEqual(51, self.guido.age)

    def test_get_friends(self):
        with mock.patch("user.fetch_vk_api") as mock_vk:
            mock_vk.return_value = ["z_50", "v_50", "f_51"]

            self.assertEqual(self.guido.get_friends(), ["z_50", "v_50", "f_51"])
            expected_calls = [
                mock.call("/friends", "Guido", None),
            ]
            self.assertEqual(expected_calls, mock_vk.mock_calls)

            mock_vk.return_value = ["z_51"]

            self.assertEqual(self.guido.get_friends(age="51"), ["z_51"])
            expected_calls = [
                mock.call("/friends", "Guido", None),
                mock.call("/friends", "Guido", "51"),
            ]
            self.assertEqual(expected_calls, mock_vk.mock_calls)

    def test_get_friends_several(self):
        with mock.patch("user.fetch_vk_api") as mock_vk:
            mock_vk.side_effect = ["z_50", "v_50", "f_51"], ["z_51"]

            self.assertEqual(self.guido.get_friends(), ["z_50", "v_50", "f_51"])
            expected_calls = [
                mock.call("/friends", "Guido", None),
            ]
            self.assertEqual(expected_calls, mock_vk.mock_calls)

            self.assertEqual(self.guido.get_friends(age="51"), ["z_51"])
            expected_calls = [
                mock.call("/friends", "Guido", None),
                mock.call("/friends", "Guido", "51"),
            ]
            self.assertEqual(expected_calls, mock_vk.mock_calls)

            #self.assertEqual(self.guido.get_friends(age="51"), ["z_51"])

    def test_get_friends_failed(self):
        with mock.patch("user.fetch_vk_api") as mock_vk:
            mock_vk.side_effect = ValueError("WRONG")

            with self.assertRaises(ValueError) as err:
                self.guido.get_friends()

            self.assertEqual(str(err.exception), "WRONG")
