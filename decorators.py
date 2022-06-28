import time

from usefull_decorators.patterns import Singleton, builder_function, Observable


def changeling(q):
    print(q)


@Observable(attach=[("t", changeling)])
class Test:
    def __init__(self, t: str, t2: bool = False):
        self.t = t
        self.t2 = t2

    def tb1(self, t):
        self.t = t

    def tb2(self, t2):
        self.t2 = t2


q1 = Test("test")
q1.t = "hello"