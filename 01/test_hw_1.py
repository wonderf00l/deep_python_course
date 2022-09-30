import builtins
import unittest
from unittest.mock import patch, Mock
import hw1
from hw1 import TicTacGame


class TicTacTest(unittest.TestCase):


    @staticmethod
    def mock_print():
        """
           Mock-функция для выброса исключения
           и выхода из бесконечного цикла при вводе данных
        """
        print("Неверный ввод, попробуйте снова")
        raise Exception


    @staticmethod
    def mock_start_game(TicTac_obj, case):
        """
            Mock-функция start_game без ввода параметров
        """
        TicTac_obj.size = 3
        TicTac_obj.board = case
        count = 0
        while True:
            TicTac_obj.show_board()
            if count >= 2:
                if TicTac_obj.check_winner():
                    break
            if count >= 2:
                if TicTac_obj.check_winner():
                    TicTac_obj.show_board()
                    break
            count += 1
        while True:
            try:
                input_ = input("Рестарт?(Да/Нет)")
                if input_ == "Да":
                    TicTac_obj.start_game()
                else:
                    if input_ != "Нет":
                        raise ValueError
                    return
            except ValueError:
                print("Некорректный ввод, попробуйте снова")


    @patch("builtins.input")
    def test_create_board_valid(self, mock_input):
        game = TicTacGame()
        mock_input.return_value = 3
        game.create_board()
        self.assertEqual(game.board, [['_','_','_'],['_','_','_'],['_','_','_']])

    # Подобный метод замены функции(в частности print) не покрывает оригинальные функции в тесте
    # Потому покрытие неполное
    # Хотелось бы понять, какие ходы можно использовать для покрытия этих веток
    @patch("builtins.input")
    def test_create_board_invalid_int(self, mock_input):
        game = TicTacGame()
        mock_input.return_value = 2
        builtins.print = Mock(side_effect=self.mock_print)
        with self.assertRaises(Exception):
            game.create_board()


    @patch("builtins.input")
    def test_create_board_str(self, mock_input):
        game = TicTacGame()
        mock_input.return_value = 'str'
        builtins.print = Mock(side_effect=self.mock_print)
        with self.assertRaises(Exception):
            game.create_board()


    @patch("builtins.print")
    def test_show_board(self, mock_print):
        game = TicTacGame()
        game.board = [['_','_','_'],['_','_','_'],['_','_','_']]
        game.show_board()
        mock_print.assert_called_with('_', '_', '_', sep=' ')


    @patch("builtins.input")
    def test_validate_input_valid(self, mock_input):
        game = TicTacGame()
        game.size = 3
        mock_input.return_value = 2
        for value in game.validate_input().values():
            if value != mock_input.return_value - 1:
                raise AssertionError
        self.assertTrue(True)


    @patch("builtins.input")
    def test_validate_input_invalid_int(self, mock_input):
        game = TicTacGame()
        mock_input.return_value = 10
        builtins.print = Mock(side_effect=self.mock_print)
        with self.assertRaises(Exception):
            game.validate_input()


    @patch("builtins.input")
    def test_validate_input_str(self, mock_input):
        game = TicTacGame()
        mock_input.return_value = "str"
        builtins.print = Mock(side_effect=self.mock_print)
        with self.assertRaises(Exception):
            game.validate_input()


    @patch("hw1.TicTacGame.validate_input")
    def test_fill_the_field_valid(self, mock_validate_input):
        game = TicTacGame()
        game.board = [['_','_','_'],['_','_','_'],['_','_','_']]
        mock_validate_input.return_value = {'position_row': 2, 'position_col': 2}
        game.fill_the_field('X')
        self.assertEqual('X', game.board[2][2])


    @patch("hw1.TicTacGame.validate_input")
    def test_fill_the_field_same_value(self, mock_validate_input):
        game = TicTacGame()
        game.board = [['X', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
        mock_validate_input.return_value = {'position_row': 1, 'position_col': 1}
        game.fill_the_field('X')
        builtins.print = Mock(side_effect=self.mock_print)
        with self.assertRaises(Exception):
            game.fill_the_field()


    def test_is_full(self):
        game = TicTacGame()
        game.board = [['X', 'X', 'X'], ['X', 'X', 'X'], ['X', 'X', 'X']]
        self.assertTrue(game.is_full())


    def test_is_full_falsy(self):
        game = TicTacGame()
        game.board = [['X', '_', 'X'], ['X', 'X', 'X'], ['X', '_', 'X']]
        self.assertFalse(game.is_full())


    @patch("builtins.print")
    def test_check_winner(self, mock_print):
        x_cases = {

                    "case1":[

                            ['X', 'X', 'X'],
                            ['X', 'O', 'O'],
                            ['O', 'X', 'X']

                            ],

                    "case2":[

                            ['X', 'O', 'O'],
                            ['X', 'X', 'X'],
                            ['O', 'X', 'O']

                            ],

                    "case3":[

                            ['X', 'O', 'O'],
                            ['O', 'O', 'X'],
                            ['X', 'X', 'X']

                            ],

                    "case4":[

                            ['X', 'O', 'X'],
                            ['X', 'O', 'O'],
                            ['X', 'X', 'O']

                            ],

                    "case5":[

                            ['O', 'X', 'X'],
                            ['X', 'X', 'O'],
                            ['O', 'X', 'X']

                            ],

                    "case6":[

                            ['X', 'O', 'X'],
                            ['X', 'O', 'X'],
                            ['O', 'X', 'X']

                            ],

                    "case7":[

                            ['X', 'O', 'O'],
                            ['X', 'X', 'O'],
                            ['O', 'X', 'X']

                            ],

                    "case8":[

                            ['X', 'O', 'X'],
                            ['O', 'X', 'O'],
                            ['X', 'X', 'O']

                            ]

                  }
        o_cases = {

                    "case1":[

                            ['O', 'O', 'O'],
                            ['X', 'X', 'O'],
                            ['O', 'X', 'X']

                            ],

                    "case2":[

                            ['X', 'O', 'X'],
                            ['O', 'O', 'O'],
                            ['X', 'X', 'O']

                            ],

                    "case3":[

                            ['X', 'O', 'O'],
                            ['O', 'X', 'X'],
                            ['O', 'O', 'O']

                            ],

                    "case4":[

                            ['O', 'O', 'X'],
                            ['O', 'X', 'O'],
                            ['O', 'X', 'O']

                            ],

                    "case5":[

                            ['O', 'O', 'X'],
                            ['X', 'O', 'O'],
                            ['O', 'O', 'X']

                            ],

                    "case6":[

                            ['O', 'X', 'O'],
                            ['O', 'X', 'O'],
                            ['X', 'X', 'O']

                            ],

                    "case7":[

                            ['O', 'O', 'X'],
                            ['X', 'O', 'O'],
                            ['O', 'X', 'O']

                            ],

                    "case8":[

                            ['X', 'O', 'O'],
                            ['X', 'O', 'O'],
                            ['O', 'X', 'O']

                            ]

                  }
        game = TicTacGame()
        game.size = 3
        for x_case,o_case in zip(x_cases.values(),o_cases.values()):
            game.board = x_case
            if not game.check_winner():
                raise AssertionError
            game.board = o_case
            if not game.check_winner():
                raise AssertionError


    @patch("builtins.print")
    def test_check_winner_draw(self, mock_print):
        game = TicTacGame()
        game.size = 3
        game.board = [

                        ['O', 'O', 'X'],
                        ['X', 'X', 'O'],
                        ['O', 'X', 'O']

                     ]
        game.check_winner()
        mock_print.assert_called_with("Ничья")


    def test_check_winner_falsy(self):
        game = TicTacGame()
        game.size = 3
        game.board = [

            ['O', '_', 'X'],
            ['_', 'X', 'O'],
            ['O', '_', 'O']

        ]
        self.assertFalse(game.check_winner())


    @patch("builtins.print")
    @patch("builtins.input")
    def test_start_game_x_case(self, mock_input, mock_print): #важен порядок передачи аргументов при многоразовом использовании @patch
        game = TicTacGame()
        x_case = [

                    ['X', 'O', 'O'],
                    ['O', 'O', 'X'],
                    ['X', 'X', 'X']

                 ]
        game.start_game = Mock(side_effect=self.mock_start_game)
        mock_input.return_value = "Нет"
        self.mock_start_game(game, x_case)
        mock_print.assert_called_with("Выиграли крестики")


    @patch("builtins.print")
    @patch("builtins.input")
    def test_start_game_o_case(self, mock_input, mock_print):
        game = TicTacGame()
        o_case = [

            ['X', 'O', 'O'],
            ['O', 'O', 'X'],
            ['X', 'O', 'X']

        ]
        game.start_game = Mock(side_effect=self.mock_start_game)
        mock_input.return_value = "Нет"
        self.mock_start_game(game, o_case)
        mock_print.assert_called_with("Выиграли нолики")


    @patch("builtins.print")
    @patch("builtins.input")
    def test_start_game_draw(self, mock_input, mock_print):
        game = TicTacGame()
        o_case = [

            ['X', 'X', 'O'],
            ['O', 'O', 'X'],
            ['X', 'O', 'X']

        ]
        game.start_game = Mock(side_effect=self.mock_start_game)
        mock_input.return_value = "Нет"
        self.mock_start_game(game, o_case)
        mock_print.assert_called_with("Ничья")


if __name__ == '__main__':
    unittest.main()
