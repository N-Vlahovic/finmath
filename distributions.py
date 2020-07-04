from collections.abc import Iterator
import math
from typing import Tuple

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


class BoxMueller(Iterator):
    """
    The Box-Mueller transform takes two independent U(0,1) random variables U1, U2
    to generate two independent N(0,1) random variables Z1, Z2.
    """
    def __init__(
        self,
        rand_u1: pseudo_random.RandomSequence,
        rand_u2: pseudo_random.RandomSequence,
        mu: float = 0,
        sigma: float = 1,
    ) -> None:
        self.mu = mu
        self.sigma = sigma
        self.generator = self.bm(sigma=sigma, mu=mu, rand_u1=rand_u1, rand_u2=rand_u2)

    def __next__(self) -> Tuple[float, float]:
        return self.generator.__next__()

    @classmethod
    def bm(
        cls,
        sigma: float,
        mu: float,
        rand_u1: pseudo_random.RandomSequence,
        rand_u2: pseudo_random.RandomSequence,
    ):
        while True:
            u1, u2 = next(rand_u1), next(rand_u2)
            z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
            yield z1 * sigma + mu, z2 * sigma + mu


class RandomWalk(Iterator):
    def __init__(
            self,
            rand_u1: pseudo_random.RandomSequence,
            rand_u2: pseudo_random.RandomSequence,
            n: int,
            seed: Tuple[float, float] = (1.0, 1.0),
            mu: float = 0,
            sigma: float = 1,
    ) -> None:
        bm = BoxMueller(sigma=sigma, mu=mu, rand_u1=rand_u1, rand_u2=rand_u2)
        self.generator = self.sequence(n=n, sigma=sigma, mu=mu, bm=bm, seed=seed)

    def __next__(self) -> Tuple[float, float]:
        return self.generator.__next__()

    @classmethod
    def sequence(
        cls,
        n: int,
        sigma: float,
        mu: float,
        seed: Tuple[float, float],
        bm: BoxMueller,
    ):
        h = 1 / n
        w1, w2 = seed
        while True:
            yield w1, w2
            z1, z2 = next(bm)
            w1 = w1 * math.exp((mu - 0.5 * sigma ** 2) * h + sigma * math.sqrt(h) * z1)
            w2 = w2 * math.exp((mu - 0.5 * sigma ** 2) * h + sigma * math.sqrt(h) * z2)
