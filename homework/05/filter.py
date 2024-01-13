import io
from functools import singledispatch


@singledispatch
def file_filter(file_arg: str, keywords):
    with open(file_arg, 'r', encoding='UTF-8') as text:
        for string in text:
            for word in keywords:
                if word.lower() in string.lower().split():
                    yield string.rstrip('\n')
                    break


@file_filter.register(io.TextIOWrapper)
def _filter(file_obj_arg: io.TextIOWrapper, keywords):
    for string in file_obj_arg:
        for word in keywords:
            if word.lower() in string.lower().split():
                yield string.rstrip('\n')
                break


if __name__ == "__main__":
    FILE_NAME = "some_text.txt"

    with open(FILE_NAME, 'r', encoding='UTF-8') as file:
        gen_obj = file_filter(file, ['hello', 'роза', '123'])
        for item in gen_obj:
            print(f"{FILE_NAME}: {item}")
        print(f"End for {FILE_NAME}", end='\n'*2)

    print("Now with str arg: ")
    gen_obj_1 = file_filter(FILE_NAME, ['hello', 'роза', '123'])
    for item_1 in gen_obj_1:
        print(f"{FILE_NAME}: {item_1}")
