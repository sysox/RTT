import json
import math
from scipy.stats import binom, norm, multinomial, chi2, uniform, kstwobign
from scipy.stats import binomtest, norm, chisquare#‘two-sided’, ‘greater’, ‘less’
import matplotlib.pyplot as plt
import numpy as np
from multinomial import multinomial_events

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




def multinomial_data(n=6, probs=[1/3]*3):
    M = multinomial_events(n = 6, probs = [1/3]*3)
    M.events_data()
    res = {}
    res['events'] = M.dist['events_stat']
    res['events_pmf'] = M.dist['events_pmf']

    res['less'] = M.dist['less']
    res['greater'] = M.dist['greater']
    res['greater'] = M.dist['greater']
    res['two-sided'] = M.dist['two-sided']
    return res

def chi2_data(x, df=2):
    res = {}
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
    probs = [1/num_bins]*num_bins

    M = multinomial_data(n=39, probs=probs)
    x = M['events']
    Ch = chi2_data(x=x, df=df)


