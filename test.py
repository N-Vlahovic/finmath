import matplotlib.pyplot as plt
from pseudo_random import Generators, RandomSequence
from distributions import AcceptanceRejection, RandomWalk, BoxMueller


ru = RandomSequence(Generators.halton, base=2)
ry = RandomSequence(Generators.halton, base=3)
# ry = RandomSequence(Generators.lcg)
# walk = RandomWalk(rand_u1=ru, rand_u2=ry, n=1000)
walk = BoxMueller(rand_u1=ru, rand_u2=ry)
data = [next(walk) for _ in range(1000)]
for _ in range(10):
    print(next(walk))
plt.hist([_[0] for _ in data])
plt.hist([_[1] for _ in data])
plt.savefig('p.png')
