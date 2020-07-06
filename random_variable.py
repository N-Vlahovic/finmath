import distributions
import pseudo_random

import math


class AbstractRandomVariable:
    def __init__(self, uni: pseudo_random.RandomSequence, **kwargs) -> None:
        self.uni = uni
        self.generator = self.sequence(uni=uni, **kwargs)

    def __next__(self) -> float:
        return self.generator.__next__()

    @classmethod
    def sequence(cls, *args, **kwargs):
        yield 0


class ExponentialRandomVariable(AbstractRandomVariable):
    @classmethod
    def sequence(cls, uni: pseudo_random.RandomSequence, lmbda: float):
        yield distributions.exp_inv_sampling(next(uni), lmbda=lmbda)
