import json
import math
from scipy.stats import binom, norm, multinomial, chi2, uniform, kstwobign
from scipy.stats import binomtest, norm, chisquare#‘two-sided’, ‘greater’, ‘less’
import matplotlib.pyplot as plt
import numpy as np
from itertools import product
from collections import defaultdict

def pvalue2(pLeft, pRight):
    # tested on binomial scipy - correct results
    tmp = min(pLeft, pRight)
    if tmp >= 0.5:
        tmp = 0.5

    return 2*tmp
def binomial_data(n=100, p=0.5):
    res = {}
    outcomes = np.arange(0, n + 1)
    res['outcomes'] = outcomes
    res['pmf'] = binom.pmf(outcomes, n=n, p=p)
    for alternative in ['less', 'greater', 'two-sided']:
       res[alternative] = np.array([binomtest(k, n, p = p, alternative=alternative).pvalue for k in outcomes])
    return res
def normal_data(x = 1000 , mean = 0, std = 1):
    res = {}
    if type(x) == int:
        x = np.arange(0, x + 1)
    else:
        x = np.array(x)
    res['outcomes'] = x
    res['pdf'] = np.array(norm.pdf(x, mean, std))
    res['less'] = np.array(norm.cdf(x, mean, std))
    res['greater'] = np.array([1]*len(x)) - res['less']
    res['two-sided'] = 2*np.minimum(res['less'], res['greater'])

    return res
def sum_vectors(size, vector_sum):
    return np.array([tuple(k) for k in product(range(vector_sum+1),repeat=size)if sum(k)==vector_sum])
def multinomial_data(n=6, p=[1/3]*3):
    res = {}
    sample_space = sum_vectors(len(p), vector_sum=n)
    outcomes_probs = multinomial.pmf(sample_space, n=n, p=p)

    # outcomes sorted according to chi2stats
    f_exp = np.round(n * np.array(p))
    if sum(f_exp) != n:
        print("Warning: sum(f_exp) != n")
        return None
    E = int(f_exp[0])
    chi2stats = [chisquare(f_obs=f_obs, f_exp=f_exp).statistic
                 for f_obs, outcomes_prob in zip(sample_space, outcomes_probs)]
    chi2stats_ints = np.round(np.array(chi2stats)*E) # normalized to ints

    #sorting according chi2stats
    # print(*zip(chi2stats_ints, sample_space, outcomes_probs), sep='\n')
    idx = np.argsort(chi2stats_ints)
    chi2stats_ints = chi2stats_ints[idx]
    sample_space = sample_space[idx]
    outcomes_probs = outcomes_probs[idx]
    # print(*zip(chi2stats_ints, sample_space, outcomes_probs), sep='\n')
    res['outcomes'] = sample_space
    res['pmf'] = outcomes_probs


    # outcome to event grouping (according to chi2stat)
    event_probs = {}
    samples = {}
    for idx in range(len(chi2stats_ints)):
        chi2stat_int = chi2stats_ints[idx]
        prob = outcomes_probs[idx]
        sample = sample_space[idx]
        if chi2stat_int not in event_probs:
            event_probs[chi2stat_int] = prob
            samples[chi2stat_int] = [sample]
        else:
            event_probs[chi2stat_int] += prob
            samples[chi2stat_int].append(sample)
    x = np.array(list(event_probs.keys())) / E
    res['events'] = x
    res['events_pmf'] = np.array(list(event_probs.values()))
    res['samples'] = samples.values()

    res['less'] = np.cumsum(res['events_pmf'])
    res['greater'] = np.array([1] * len(x)) - res['less'] + res['events_pmf']
    res['two-sided'] = np.array([pvalue2(pLeft, pRight) for pLeft, pRight in zip(res['less'], res['greater'])])
    return res

def chi2_data(x = 10, df=2):
    res = {}
    if type(x) == int:
        x = np.arange(0, x + 1)
    else:
        x = np.array(x)
    res['events'] = x
    res['events_pdf'] = np.array(chi2.pdf(x, df))
    res['less'] = np.array(chi2.cdf(x, df))
    res['greater'] = np.array([1]*len(x)) - res['less']
    res['two-sided'] = 2*np.minimum(res['less'], res['greater'])
    return res


if __name__ == '__main__':
    # binomial vs normal
    n = 98 # number of trials
    p = 0.4 # probability of success
    B = binomial_data(n=n, p=p)
    N = normal_data(x=np.arange(0, n+1), mean=n*p, std=math.sqrt(n*p*(1-p)))

    # chi2 vs multinomial
    num_bins = 3
    df = num_bins - 1
    p = [1/num_bins]*num_bins

    M = multinomial_data(n=39, p=p)
    x = M['events']
    Ch = chi2_data(x=x, df=df)


