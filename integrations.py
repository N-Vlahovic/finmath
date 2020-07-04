from collections.abc import Callable

import pseudo_random
import utils


class AbstractIntegrator:
    @classmethod
    def integrate(cls, *args, **kwargs):
        pass


class MonteCarlo(AbstractIntegrator):
    @classmethod
    def integrate(
        cls,
        fun: Callable,
        uni: pseudo_random.RandomSequence,
        a: float,
        b: float,
        n: int,
    ) -> float:
        return sum(fun((b - a) * next(uni) + a) for _ in range(n)) / n

    @classmethod
    def pi_approx(
        cls,
        n: int,
        rand_x: pseudo_random.RandomSequence,
        rand_y: pseudo_random.RandomSequence,
    ) -> float:
        pi = 0.0
        for i in range(n):
            x, y = next(rand_x), next(rand_y)
            if x**2 + y**2 < 1:
                pi += 1
        return 4 * pi / n


class Simpson(AbstractIntegrator):
    @classmethod
    def integrate(
        cls,
        fun: Callable,
        n: int,
        a: float,
        b: float,
    ) -> float:
        n = n if n % 2 == 0 else n + 1
        partition = utils.Partition(a=a, b=b, n=n)
        ans = 0.0
        for i, x in enumerate(partition):
            c = cls.coef_even_n(i=i, n=n)
            ans += c * fun(x)
        return ans * (b - a) / (n * 3)

    @classmethod
    def coef_even_n(cls, i: int, n: int) -> int:
        if i == 0 or i == n:
            return 1
        elif i % 2 == 0:
            return 2
        return 4
