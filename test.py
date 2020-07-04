import matplotlib.pyplot as plt
from pseudo_random import Generators, RandomSequence
from distributions import AcceptanceRejection


ru = RandomSequence(Generators.halton, base=2)
ry = RandomSequence(Generators.halton, base=3)
un = RandomSequence(Generators.lcg)
ar = AcceptanceRejection(rand_u=ru, rand_y=ry, uni=un)
x = [next(ar) for _ in range(1000)]
plt.hist(x, bins=50)
plt.gca().set(title='Standard Normal Distribution', ylabel='')
plt.savefig('assets/AR.png')
