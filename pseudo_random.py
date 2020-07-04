from __future__ import annotations
from collections.abc import Iterator
from enum import Enum, unique
import math
from typing import Union

import utils


class HaltonSequence(Iterator):
    BASE: int = 2

    def __init__(self, base: int = None) -> None:
        self.base = base or self.BASE
        self.generator = self.halton_sequence(base=self.base)

    def __next__(self) -> float:
        return self.generator.__next__()

    @staticmethod
    def halton_number(index: int, base: int) -> float:
        f: int = 1
        r: float = 0.0
        while index > 0:
            f /= base
            r += f * (index % base)
            index = math.trunc(index / base)
        return r

    @classmethod
    def halton_sequence(cls, base: int):
        index = 0
        while True:
            yield cls.halton_number(index=index, base=base)
            index += 1


class LCG(Iterator):
    MODULUS: int = 2**31
    MULTIPLIER: int = 65539
    INCREMENT: int = 0
    SEED: int = 1

    def __init__(
            self,
            modulus: int = None,
            multiplier: int = None,
            increment: int = None,
            seed: int = None,
            uniform: bool = True
    ) -> None:
        modulus = modulus or self.MODULUS
        multiplier = multiplier or self.MULTIPLIER
        increment = increment or self.INCREMENT
        seed = seed or self.SEED
        if self.validate_params(modulus, multiplier, increment, seed) is False:
            raise utils.ParamError()
        self.modulus = modulus
        self.multiplier = multiplier
        self.increment = increment
        self.seed = seed
        self.generator = self.lcg(modulus, multiplier, increment, seed, uniform=uniform)

    def __next__(self) -> Union[int, float]:
        return self.generator.__next__()

    @classmethod
    def validate_params(cls, modulus: int, multiplier: int, increment: int, seed: int) -> bool:
        if not modulus > 0:
            return False
        if not 0 < multiplier < modulus:
            return False
        if not 0 <= increment <= modulus:
            return False
        if not 0 <= seed < modulus:
            return False
        return True

    @staticmethod
    def lcg(modulus: int, multiplier: int, increment: int, seed: int, uniform: bool = False):
        while True:
            seed = (multiplier * seed + increment) % modulus
            yield seed if uniform is False else seed / modulus


@unique
class Generators(Enum):
    halton = HaltonSequence
    lcg = LCG


class RandomSequence(Iterator):
    def __init__(self, generator: Generators, **kwargs):
        self.generator = generator.value(**kwargs)

    def __next__(self) -> float:
        return self.generator.__next__()
