class CustomList(list):
    def __init__(self, *data):
        """Инициализация поля data с извлечением и фильтрацией данных:
        в поле data попадают только экземпляры int и float, которые могут
        находиться на любом уровне вложенности"""
        self.__data = []

        def construction(val):
            flag = 0
            for item in val:
                if isinstance(item, (str, dict, bool)):
                    continue
                if isinstance(item, (int, float)):
                    self.__data.append(item)
                    continue
                flag = 1
                construction(item)
            if not flag:
                return

        construction(data)
        self.__len = len(self.__data)
        super().__init__(self)

    def sum(self):
        return sum(self.__data)

    def __add__(self, other):
        list_ = other._CustomList__data
        l_1 = self.__len
        l_2 = len(list_)
        if min(l_1, l_2) == l_1:
            return CustomList([sum(item) for item in zip(self.__data, list_)] + list_[l_1:])
        return CustomList([sum(item) for item in zip(self.__data, list_)] + self.__data[l_2:])

    def __sub__(self, other):
        list_ = other._CustomList__data
        l_1 = len(self.__data)
        l_2 = len(list_)
        if min(l_1, l_2) == l_1:
            return CustomList([item[0] - item[1] for item in zip(self.__data, list_)] + list_[l_1:])
        return CustomList([item[0] - item[1] for item in zip(self.__data, list_)] + self.__data[l_2:])

    def __iadd__(self, other):
        if len(other) < self.__len:
            for i in range(len(other)):
                self.__data[i] += other[i]
        else:
            for j in range(self.__len):
                self.__data[j] += other[j]
            self.__data += other[self.__len:]
        return self

    def __isub__(self, other):
        if len(other) < self.__len:
            for i in range(len(other)):
                self.__data[i] -= other[i]
        else:
            for j in range(self.__len):
                self.__data[j] -= other[j]
            self.__data += other[self.__len:]
        return self

    def __radd__(self, other):
        if len(other) < self.__len:
            for i in range(len(other)):
                other[i] += self.__data[i]
            return other + self.__data[len(other):]
        for j in range(self.__len):
            other[j] += self.__data[j]
        return other

    def __rsub__(self, other):
        if len(other) < self.__len:
            for i in range(len(other)):
                other[i] -= self.__data[i]
            return other + self.__data[len(other):]
        for j in range(self.__len):
            other[j] -= self.__data[j]
        return other

    def __eq__(self, other):
        return True if self.__len == other.sum() else False

    def __ne__(self, other):
        return True if self.__len != other.sum() else False

    def __lt__(self, other):
        return True if self.__len < other.sum() else False

    def __le__(self, other):
        return True if self.__len <= other.sum() else False

    def __gt__(self, other):
        return True if self.__len > other.sum() else False

    def __ge__(self, other):
        return True if self.__len >= other.sum() else False

    def __str__(self):
        return f"список:{self.__data}, сумма: {self.sum()}"


print(print)
a = CustomList([1, [[2, 's', (3, {1: 2}, {4, 5}, [[[True, 'hello', (6, 7)]]])]]])
print(a)
b = CustomList(True, 1, [1, 's', ])
print(b)
print(b < a)
# c = b + a
# print(c)
d = [1, 1]
d -= a
print(d)
a -= [1, 1, 1, 1, 1, 1, 1, 1]
print('\n' * 3)
print(a)
# CustomList.__init__.a = 4
# print(CustomList.__init__.__dict__) # {'a': 4}
# tup = (1,2 )
# b = list(tup)
# print(b.__dir__())
# print(help(list))
# print(list.__dict__)
