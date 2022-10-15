class CustomMeta(type):
    def __new__(mcs, name, bases, class_dict, **kwargs):
        lst = [attr for attr in class_dict.keys() if attr[:2] != '__' and attr[-2:] != '__']
        for attr in lst:
            class_dict[f'custom_{attr}'] = class_dict.pop(attr)
        return super().__new__(mcs, name, bases, class_dict)

    def __call__(cls, *args, **kwargs):
        print("---CustomClass()---")
        return super().__call__(*args, **kwargs)


class Integer:
    def __set_name__(self, owner, name):
        self.__name = name
        self._attr = f"_{name}"

    def __get__(self, instance, owner):
        print('even:', end=' ') if self._attr % 2 == 0 else print('uneven:', end=' ')
        return self._attr

    def __set__(self, instance, value):
        if isinstance(value, int):
            super().__setattr__('_attr', value)
        else:
            raise AttributeError("Int only")


class String:
    def __set_name__(self, owner, name):
        self.__name = name
        self._attr = f"_{name}"

    def __get__(self, instance, owner):
        print('long str:', end=' ') if len(self._attr) > 10 else print('short str:', end=' ')
        return self._attr.capitalize() * 2

    def __set__(self, instance, value):
        if isinstance(value, str):
            super().__setattr__('_attr', value)
        else:
            raise AttributeError("Str only")


class PositiveInteger:
    def __set_name__(self, owner, name):
        self.__name = name
        self._attr = f"_{name}"

    def __get__(self, instance, owner):
        print('even positive:', end=' ') if self._attr % 2 == 0 else print('uneven positive:', end=' ')
        return self._attr

    def __set__(self, instance, value):
        if isinstance(value, int) and value > 0:
            super().__setattr__('_attr', value)
        else:
            raise AttributeError("Positive int only")


class CustomClass(metaclass=CustomMeta):
    val = 10
    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price

    def __setattr__(self, key, value):
        super().__setattr__(f'custom_{key}', value)

    @staticmethod
    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"


def foo():
    return 5


if __name__ == '__main__':
    inst = CustomClass(3, 'aaw', 2)
    print(CustomClass.__dict__)
    print(inst.custom_name)
    inst.price = 50
    print(inst.custom_price)
    inst.elem = 'added later'
    inst.elem1 = foo
    print(inst.__dict__)
