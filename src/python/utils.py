import math
import numpy as np
from itertools import product
from collections import Counter
from math import factorial
from itertools import accumulate
import time

def subset_sum_ineff(subset_size, target_sum, numbers):
    '''
    8, 8 - 6s
    9, 9 - > 30s
    '''
    return [tuple(k) for k in product(numbers, repeat=subset_size) if sum(k)==target_sum]
def subset_sum_rec(subset_size, target_sum, numbers, partial=[], partial_sum=0, partial_len = 0):
    # somehow fast:
    #   subset_size, target_sum:
    #   6, 100 => 27s,
    #   5, 100 => 5s

    if partial_sum == target_sum and partial_len == subset_size:
        yield partial
    if partial_sum >= target_sum or partial_len >= subset_size:
        return
    for i, n in enumerate(numbers):
        remaining = numbers[i:]
        yield from subset_sum_rec(subset_size, target_sum, remaining, partial + [n], partial_sum + n, partial_len + 1)
def subset_sum(subset_size, target_sum, numbers = None, repeat = False):
    if numbers == None:
        numbers = list(range(0, target_sum+1))

    if target_sum == None:
        target_sum = subset_size

    if repeat:
        yield from subset_sum_ineff(subset_size, target_sum, numbers)
    else:
        yield from subset_sum_rec(subset_size, target_sum, numbers)

def num_unique_vec_perms(vector):
    hist = Counter(vector)
    return factorial(len(vector)) // math.prod(map(factorial, hist.values()))
def multinomial_coeffs(lst):
    res, i = 1, sum(lst)
    i0 = lst.index(max(lst))
    for a in lst[:i0] + lst[i0+1:]:
        for j in range(1,a+1):
            res *= i
            res //= j
            i -= 1
    return res

def histogram(bin_edges, values):
    sorted_vals = sorted(values)
    freqs = [0]*len(bin_edges)
    idx = 0
    for val in sorted_vals:
        if val > bin_edges[idx]:
            while(val > bin_edges[idx]):
                idx += 1
                if idx > len(bin_edges) - 1:
                    print(f"value {val} not in bin_edges {bin_edges[-3:]}")

        freqs[idx] += 1
    return dict(zip(bin_edges, freqs))

if __name__ == "__main__":
    print(num_unique_vec_perms([1,1, 2,2]))
    # t0 = time.time()
    print(list(subset_sum(4,8, repeat=True)))
    # t1 = time.time()
    # print(t1-t0)



# not used yet