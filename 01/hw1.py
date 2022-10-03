class TicTacGame:


    def __init__(self):
        """Инициализация атрибутов board и size(размер доски)"""
        self.board = None
        self.size = None


    def create_board(self) -> None:
        """
        Ввод параметра размера доски, проверка ввода, создание пустой доски
        Размер может быть задан произвольно, но с учетом правил игры на выбор 3 или 4
        """
        while True:
            try:
                self.size = int(input("Введите значение ширины(длины) поля (3 или 4): ")) #Считывание размера
                if self.size not in range(3, 5):                                          #Обработка ввода
                    raise IndexError
                break
            except (ValueError, IndexError):
                print("Неверный ввод, попробуйте снова")
        self.board = []
        for i in range(self.size): #заполнение списка
            self.board.append([])
        for row in self.board:
            for j in range(self.size):
                row.append('_')


    def show_board(self) -> None:
        """Вывод доски"""
        for row in self.board:
            print(*row, sep=' ')


    def validate_input(self) -> dict:
        """
        Ввод параметров положения элемента на доске, проверка ввода
        Возможные положения: 1-3/1-4
        """
        while True:
            try:
                position_row = int(input("Введите номер строки: ")) #Считывание № строки
                if position_row < 1 or position_row > self.size:    #Проверка ввода
                    raise IndexError
                break
            except (ValueError, IndexError):
                print("Неверный ввод, попробуйте снова")
        while True:
            try:
                position_col = int(input("Введите номер столбца: ")) #Считывание № столбца
                if position_col < 1 or position_col > self.size:     #Проверка ввода
                    raise IndexError
                break
            except (ValueError, IndexError):
                print("Неверный ввод, попробуйте снова")
        return {'position_row': position_row - 1, 'position_col': position_col - 1}


    def fill_the_field(self, value: str) -> None:
        """Заполнение поля доски с учетом введеных параметров положения"""
        while True:
            field = self.validate_input() #Считывание параметров положения
            if self.board[field['position_row']][field['position_col']] == '_': #Проверка на наличие элемента в поле
                self.board[field['position_row']][field['position_col']] = value
                break
            else:
                print("В данном поле уже есть элемент")
            


    def is_full(self) -> bool:
        """Проверка доски на заполненность"""
        for row in self.board:
            for field in row:
                if field == '_':
                    return False
        return True


    def check_winner(self) -> bool:
        """
        Определение победителя
        True: победили крестики/нолики, ничья
        False: игра не завершена
        """
        for tup in zip(*self.board):  # проверка по стобцам
            if len(set(tup)) == 1 and '_' not in tup:
                if 'X' in tup:
                    print("Выиграли крестики")
                else:
                    print("Выиграли нолики")
                return True

        for row in self.board:  # проверка по строкам
            if len(set(row)) == 1 and '_' not in row:
                if 'X' in row:
                    print("Выиграли крестики")
                else:
                    print("Выиграли нолики")
                return True

        diagonal = set()
        for row_num, row in enumerate(self.board): #проверка по главной диагонали
            diagonal.add(row[row_num])
        if len(diagonal) == 1 and '_' not in diagonal:
            if 'X' in diagonal:
                print("Выиграли крестики")
            else:
                print("Выиграли нолики")
            return True

        secondary_diagonal = set()
        for row_num, row in enumerate(self.board): #проверка по побочной диагонали
            secondary_diagonal.add(row[(self.size - 1) - row_num])
        if len(secondary_diagonal) == 1 and '_' not in secondary_diagonal:
            if 'X' in secondary_diagonal:
                print("Выиграли крестики")
            else:
                print("Выиграли нолики")
            return True

        if self.is_full(): #Проверка на ничью
            print("Ничья")
            return True

        return False


    def start_game(self) -> None:
        """Запуск игры"""
        self.create_board()
        count = 0  # счетчик ходов
        while True:
            self.show_board()
            print("Ход крестиков:")
            self.fill_the_field('X')
            self.show_board()
            if count >= 2: #определение победителя начинается после 2-ого хода
                if self.check_winner():
                    break
            print("Ход ноликов:")
            self.fill_the_field('O')
            if count >= 2:
                if self.check_winner():
                    self.show_board()
                    break
            count += 1
        while True:
            try:
                input_ = input("Рестарт?(Да/Нет)") #Перезапуск/завершение
                if input_ == "Да":
                    self.start_game()
                else:
                    if input_ != "Нет":
                        raise ValueError
                    return
            except ValueError:
                print("Некорректный ввод, попробуйте снова")


# if __name__ == "__main__":
#     game = TicTacGame()
#     game.start_game()
