
from pseudo_random import Generators, RandomSequence
from distributions import AcceptanceRejection

if __name__ == '__main__':
    ru = RandomSequence(Generators.halton, base=2)
    ry = RandomSequence(Generators.halton, base=3)
    un = RandomSequence(Generators.lcg)
    ar = AcceptanceRejection(rand_u=ru, rand_y=ry, uni=un)
    for _ in range(10):
        print(next(ar))
