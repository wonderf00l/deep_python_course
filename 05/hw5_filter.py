import io
from functools import singledispatch


def processing(f_arg, keywords):
    return [
        string.rstrip('\n') for string in f_arg
        for word in keywords
        if word.lower() in string.lower().split()
    ]


@singledispatch
def file_filter(file_arg, keywords):
    with open(file_arg, 'r', encoding='UTF-8') as text:
        lst = processing(text, keywords)
        yield from lst


@file_filter.register(io.StringIO)
@file_filter.register(io.TextIOWrapper)
def _filter(file_obj_arg, keywords):
    lst = processing(file_obj_arg, keywords)
    yield from lst


if __name__ == "__main__":
    FILE_NAME = "some_text.txt"
    FILE_1 = "some_text_1.txt"
    with open(FILE_1, 'r', encoding='UTF-8') as file:
        file_obj = io.StringIO(file.read())
    gen_obj = file_filter(FILE_NAME, ['hello', 'роза', '123'])
    gen_obj_1 = file_filter(file_obj, ['hello', 'роза', '123'])
    # ggen = gen_exp_filter(FILE_NAME, ['hello', 'роза', '123'])
    for item in gen_obj:
        print(f"{FILE_NAME}: {item}")
    print(f"End for {FILE_NAME}")
    for item_1 in gen_obj_1:
        print(f"{FILE_1}: {item_1}")
