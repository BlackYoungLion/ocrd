import difflib
from functools import lru_cache

### алгоритмы ###

### Левенштейн ###
def my_dist_cached(a, b):
    @lru_cache(maxsize=len(a) * len(b))
    def recursive(i, j):
        if i == 0 or j == 0:
            return max(i, j)
        elif a[i - 1] == b[j - 1]:
            return recursive(i - 1, j - 1)
        else:
            return 1 + min(
                recursive(i, j - 1),
                recursive(i - 1, j),
                recursive(i - 1, j - 1)
            )
    return recursive(len(a), len(b))

###Коэфициент Танимото###
def tanimoto(s1, s2):
    a, b, c = len(s1), len(s2), 0.0

    for sym in s1:
        if sym in s2:
            c += 1

    return c / (a + b - c)

###Дифлиб###


def simil(s1,s2):
    matcher = difflib.SequenceMatcher(None, s1, s2)
    return matcher.ratio()