import cProfile
import pstats
import weakref
from functools import wraps
from time import time


# from memory_profiler import profile


class Computer:
    def __init__(self, cpu, gpu, ram, hdd):
        self.motherboard = MotherBoard(self)
        self.powersupply = PowerSupply(self)
        self.cpu = cpu
        self.gpu = gpu
        self.ram = ram
        self.hdd = hdd


class MotherBoard:
    def __init__(self, computer):
        self.computer = computer


class PowerSupply:
    def __init__(self, computer):
        self.computer = computer


class ComputerSlots:
    __slots__ = ("cpu", "gpu", "ram", "hdd", "motherboard", "powersupply")

    def __init__(self, cpu, gpu, ram, hdd):
        self.motherboard = MotherBoard(self)
        self.powersupply = PowerSupply(self)
        self.cpu = cpu
        self.gpu = gpu
        self.ram = ram
        self.hdd = hdd

        
class ComputerWeakref:
    def __init__(self, cpu, gpu, ram, hdd):
        self.motherboard = weakref.ref(MotherBoard(self))
        self.powersupply = weakref.ref(PowerSupply(self))
        self.cpu = cpu
        self.gpu = gpu
        self.ram = ram
        self.hdd = hdd


def timer(func):
    @wraps(func)
    def wrap(cls, quantity, *args, **kwargs):
        start = time()
        res = func(cls, quantity, *args, **kwargs)
        print(f"{func.__name__} of {cls} took {time() - start} sec")
        return res

    return wrap


def profile_deco(func):
    @wraps(func)
    def wrap_(cls, quantity, *args, **kwargs):
        prof = cProfile.Profile()
        prof.enable()
        func(cls, quantity, *args, **kwargs)
        prof.disable()
        with open("profile_stat.txt", "a+", encoding="utf-8") as file:
            ps_obj = pstats.Stats(prof, stream=file).sort_stats("cumulative")
            ps_obj.print_stats()

        def print_stat():
            with open("profile_stat.txt", "r", encoding="utf-8") as file_:
                print(file_.read())

        def del_stat():
            with open("profile_stat.txt", "w+", encoding="utf-8") as file_:
                file_.seek(0)

        wrap_.print_stat = print_stat
        wrap_.del_stat = del_stat


    return wrap_


@profile_deco
@timer
def processing(cls, quantity, *args, **kwargs):
    instances = [cls(*args, **kwargs) for _ in range(quantity)]
    for inst in instances:
        attr_lst = [getattr(inst, attr)
                    for attr in dir(inst) if attr[:2] != '__' and attr[-2:] != '__']
        for attr in attr_lst:
            if isinstance(attr, str):
                attr.upper()
    return instances


# @profile
def main():
    arg = ["cpu", "gpu", "ram", "hdd"]
    quantity = 5000
    res_1 = processing(Computer, quantity, *arg)
    del res_1
    res_2 = processing(ComputerSlots, quantity, *arg)
    del res_2
    # res_3 = processing(ComputerWeakref, quantity, *arg)
    # del res_3
    processing.print_stat()
    # processing.del_stat()


if __name__ == "__main__":  # maiN()
    main()
