import random

import scrat as sc


@sc.stash()
def func(i):
    return random.randbytes(random.randint(1000, 5000))


if __name__ == "__main__":
    for i in range(20):
        func(i)
