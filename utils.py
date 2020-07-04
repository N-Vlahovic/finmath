from collections.abc import Iterator
import math


INF: float = float('inf')


class Partition(Iterator):
    def __init__(self, a: float, b: float, n: int) -> None:
        self.a = a
        self.b = b
        self.n = n
        self.generator = self.partition_sequence(a=a, b=b, n=n)

    def __next__(self) -> float:
        return self.generator.__next__()

    @classmethod
    def partition_sequence(cls, a: float, b: float, n: int):
        c, h = a, (b - a) / n
        for _ in range(n + 1):
            yield c
            c += h


class Primes(Iterator):
    def __init__(self, seed: int = 2) -> None:
        self.seed = seed
        self.generator = self.prime_sequence(seed=self.seed)

    def __next__(self) -> int:
        return self.generator.__next__()

    @staticmethod
    def is_prime(n: int) -> bool:
        if n == 2 or n == 3 or n == 5:
            return True
        if n < 2 or n % 2 == 0:
            return False
        for x in range(3, round(math.sqrt(n)) + 1):
            if n % x == 0:
                return False
        return True

    @classmethod
    def prime_sequence(cls, seed: int = 2):
        n = seed
        while True:
            yield n
            n += 1
            while cls.is_prime(n) is False:
                n += 1


class ParamError(ValueError):
    pass
