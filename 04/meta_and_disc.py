class CustomMeta(type):
    def __new__(mcs, name, bases, class_dict, **kwargs):
        lst = [attr for attr in class_dict.keys() if attr[:2] != '__' and attr[-2:] != '__']
        for attr in lst:
            class_dict[f'custom_{attr}'] = class_dict.pop(attr)

        def __setattr__(inst_, key, value):
            inst_.__dict__[f"custom_{key}"] = value

        class_dict["__setattr__"] = __setattr__

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
    x = 50

    def __init__(self, val=99):
        self.val = val

    @staticmethod
    def line():
        return 100

    def __str__(self):
        return "Custom_by_metaclass"


class A:
    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price


def foo():
    return 5


def main_custom():
    inst = CustomClass()
    print(inst.custom_x == 50)
    print(inst.custom_val == 99)
    print(inst.custom_line() == 100)
    print(CustomClass.custom_x == 50)
    print(str(inst) == "Custom_by_metaclass")

    inst.dynamic = "added later"
    print(inst.custom_dynamic == "added later")
    try:
        inst.dynamic
    except AttributeError:
        print("No attr 'dynamic'")

    try:
        inst.x
    except AttributeError:
        print("No attr 'x'")

    try:
        inst.val
    except AttributeError:
        print("No attr 'val'")

    try:
        inst.line()
    except AttributeError:
        print("No attr 'line")

    try:
        inst.yyy
    except AttributeError:
        print("No attr 'yyy'")

    try:
        CustomClass.x
    except AttributeError:
        print("No attr 'x'")


def main_descriptors():
    inst = A(50, "Tom", 100)
    print(inst.num)
    print(inst.name)
    print(inst.price)
    inst.num = 2
    print(inst.num)
    inst.name = "James"
    print(inst.name)
    inst.price = 25
    print(inst.price)


if __name__ == '__main__':
    main_custom()
    print('\n')
    main_descriptors()
