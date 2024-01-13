from typing import Any, NewType, Union, Iterable, Sequence, Generator, Callable, TypeVar

from lib_filter import add_num

DEBUG = True


Age = Union[int, float]
Fareng = int | float
OptFareng = Fareng | None  # Optional[Fareng]

Celsius = NewType("Celsius", int)

T = TypeVar("T")


def apply_operation(
    fn: Callable[[T, T], T],
    a: T,
    b: T,
) -> T:
    return fn(a, b)


def add_str(a: str, b: str) -> str:
    return a + b


res1: int = apply_operation(add_num, 1, 22)
res2: str = apply_operation(add_str, "1", "22")

print("RES", res1, res2)


def deco(fn: Callable) -> Callable[[str], str]:
    def inner(*args, **kwargs) -> Any:
        return fn(*args, **kwargs)
    return inner


@deco
def calc_nums(a: int) -> int:
    return a


# calc_nums(1)


def gen_nums() -> Generator[int, None, str]:
    yield 10
    yield 20
    yield 30

    return "finish"  # StopIteration("finish")


def convert_c_to_f(cels: Celsius) -> Fareng:
    return cels * 9 / 5 + 32


def get_max_temp(temperatures: list[Fareng]) -> OptFareng:
    if not temperatures:
        return None

    return max(temperatures)


def get_min_temp(temperatures: Iterable[Fareng]) -> OptFareng:
    if not temperatures:
        return None

    return min(temperatures)


def get_first_temp(temperatures: Sequence[Fareng]) -> OptFareng:
    if not temperatures:
        return None

    return temperatures[0]


class User:
    def __init__(self, name):
        self.id = f"User[{name}]"


def make_request(url: str) -> dict[str, int | str]:
    return {"name": "Sol", "age": 45}


def fetch_user_data(user: User) -> dict[str, int | str]:
    user_id: int = user.id

    if DEBUG:
        url = f"http://domain.org/123"
    else:
        url = f"http://domain.org/{user.id}"

    result = make_request(url)

    return result


if __name__ == "__main__":
    sol = User("Sol")
    fetch_user_data(sol)

    # fetch_user_data("Sol")

    c1 = Celsius(42)
    print(type(c1), type(c1 + 1))

    convert_c_to_f(c1)
    faren = convert_c_to_f(c1)

    max_temp1: OptFareng = get_max_temp([1, 2, 3])
    # max_temp2: OptFareng = get_max_temp(["1", "2", "3"])  # wrong

    max_temp2: OptFareng = get_max_temp([])
    # max_temp3: OptFareng = get_max_temp((2, 3))  # wrong

    print("MAX", max_temp1, max_temp2)

    min_temp1: OptFareng = get_min_temp([1, 2, 3])
    min_temp2: OptFareng = get_min_temp((2, 3))
    min_temp3: OptFareng = get_min_temp({2, 3})
    min_temp4: OptFareng = get_min_temp(gen_nums())
    print("MIN", min_temp1, min_temp2, min_temp3, min_temp4)

    first_temp1: OptFareng = get_first_temp([1, 2, 3])
    first_temp2: OptFareng = get_first_temp((1, 2, 3))
    # first_temp3: OptFareng = get_first_temp({1, 2, 3})  # wrong
    # first_temp4: OptFareng = get_first_temp(gen_nums())  # wrong
    print("FIRST", first_temp1, first_temp2)

    result1: Any = add_num(1, 22)
    # result2 = add_num("1", "22")  # wrong
    print("ADD", result1)

