from itertools import zip_longest


class CustomListIterator:
    def __init__(self, custom_lst):
        self.lst = custom_lst
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.lst):
            val = self.lst[self.index]
            self.index += 1
            return val
        raise StopIteration("Итератор кастомного списка исчерпан")


class CustomList(list):
    def __init__(self, *data):
        """Инициализация поля data с извлечением и фильтрацией данных:
        в поле data попадают только экземпляры int и float, которые могут
        находиться на любом уровне вложенности"""
        self.__data = []

        def construction(val):
            flag = 0
            for item in val:
                if isinstance(item, dict):
                    for inner_item in list(item.items()):
                        construction(inner_item)
                    continue
                if isinstance(item, (str, bool)):
                    continue
                if isinstance(item, (int, float)):
                    self.__data.append(item)
                    continue
                flag = 1
                construction(item)
            if not flag:
                return

        construction(data)
        self.__sum = sum(self)

    @property
    def __data(self):
        return self.data

    @__data.setter
    def __data(self, val):
        self.data = val
        self.__sum = sum(self)
    
    def __iter__(self):
        return CustomListIterator(self.__data)

    def __add__(self, other):
        return CustomList([sum(item) for item in zip_longest(self, other, fillvalue=0)])

    def __sub__(self, other):
        return CustomList([item[0] - item[1] for item in zip_longest(self, other, fillvalue=0)])

    def __iadd__(self, other):
        self.__data = [sum(item) for item in zip_longest(self, other, fillvalue=0)]
        return self

    def __isub__(self, other):
        self.__data = [item[0] - item[1] for item in zip_longest(self, other, fillvalue=0)]
        return self

    # старая реализация с присоединением оставшейся части большего списка
    # def __isub__(self, other):
    #     len_ = len(self)
    #     if len(other) < len_:
    #         for i in range(len(other)):
    #             self.__data[i] -= other[i]
    #     else:
    #         for j in range(len_):
    #             self.__data[j] -= other[j]
    #         self.__data += other[len_:]
    #     return self

    def __radd__(self, other):
        other = [sum(item) for item in zip_longest(self, other, fillvalue=0)]
        return other

    def __rsub__(self, other):
        other = [item[0] - item[1] for item in zip_longest(other, self, fillvalue=0)]
        return other

    def __eq__(self, other):
        return True if self.__sum == sum(other) else False

    def __ne__(self, other):
        return True if self.__sum != sum(other) else False

    def __lt__(self, other):
        return True if self.__sum < sum(other) else False

    def __le__(self, other):
        return True if self.__sum <= sum(other) else False

    def __gt__(self, other):
        return True if self.__sum > sum(other) else False

    def __ge__(self, other):
        return True if self.__sum >= sum(other) else False

    def __str__(self):
        return f"список:{self.__data}, сумма: {self.__sum}"


if __name__ == '__main__':
    a = CustomList([1, [[2, 's', (3, {4: 5}, {6}, [[[True, 'hello', (7)]]])]]], 's', 8, '9', {(9): (10)})
    b = CustomList([1, 1, 1])
    print(a)  # список:[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], сумма: 55
    print(b)  # список:[1, 1, 1], сумма: 3
    print(a + b, '\t', b + a)
    print(a - b, '\t', b - a)
    a += b
    print(a)  # список:[2, 3, 4, 4, 5, 6, 7, 8, 9, 10], сумма: 58
    a -= b
    print(a)  # список:[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], сумма: 55
    print(a + [1, 1], '\t', [1, 1] + a)
    a -= [1, 1]
    print(a)  # список:[0, 1, 3, 4, 5, 6, 7, 8, 9, 10], сумма: 53
    a -= [1] * 10
    print(a)  # список:[-1, 0, 2, 3, 4, 5, 6, 7, 8, 9], сумма: 43
    c = [1, 1]
    c += a
    print(c)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(a < b)
    print(a >= [1, 2])
