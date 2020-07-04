from collections.abc import Iterator
import math

import pseudo_random
import utils


def exp_d(x: float, lmbda: float) -> float:
    return -math.log(1 - x) / lmbda


class AcceptanceRejection(Iterator):
    def __init__(
        self,
        rand_u: pseudo_random.RandomSequence,
        rand_y:  pseudo_random.RandomSequence,
        uni:  pseudo_random.RandomSequence
    ) -> None:
        self.rand_u = rand_u
        self.rand_y = rand_y
        self.uni = uni
        self.generator = self.ar(rand_u=rand_u, rand_y=rand_y, uni=uni)

    def __next__(self) -> float:
        return self.generator.__next__()

    @staticmethod
    def ar(
        rand_u: pseudo_random.RandomSequence,
        rand_y: pseudo_random.RandomSequence,
        uni: pseudo_random.RandomSequence,
    ):
        while True:
            u, y = utils.INF, 1
            while u > math.exp(-0.5 * (y - 1)**2):
                u, y = next(rand_u), exp_d(next(rand_y), 1)
            if next(uni) < 0.5:
                yield y
            else:
                yield -y
