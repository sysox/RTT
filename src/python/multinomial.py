import collections
import math

import numpy as np
from math import factorial, prod
from itertools import product
from itertools import permutations
from collections import defaultdict, Counter

import scipy.stats


def subset_sum_ineff(subset_size, target_sum, Set):
    '''
    8, 8 - 6s
    9, 9 - > 30s
    '''
    return [tuple(k) for k in product(Set, repeat=subset_size) if sum(k)==target_sum]
def subset_sum_recursive(subset_size, target_sum, super_set, partial_subset=[], partial_sum=0, partial_len = 0):
    # somehow fast:
    #   subset_size, target_sum:
    #   6, 100 => 27s,
    #   5, 100 => 5s

    if partial_sum == target_sum and partial_len == subset_size:
        yield partial_subset
    if partial_sum >= target_sum or partial_len >= subset_size:
        return
    for i, n in enumerate(super_set):
        remaining = super_set[i:]
        yield from subset_sum_recursive(subset_size, target_sum, remaining, partial_subset + [n], partial_sum + n, partial_len + 1)
def subset_sum(subset_size, target_sum, Set = None, unique_perms = True):
    if Set == None:
        pool_set = list(range(0, target_sum+1))
    if target_sum == None:
        target_sum = subset_size
    if unique_perms:
        yield from subset_sum_recursive(subset_size, target_sum, Set)
    else:
        yield from subset_sum_ineff(subset_size, target_sum, Set)

def chi2_stat_as_int(f_obs, f_exp):
    return sum([(O-E)*(O-E) for O, E in zip(f_obs, f_exp)])

def num_equivalent_perms(vector):
    # [1, 1, 2, 2, 3] == [1, 3, 2, 2, 1]
    hist = Counter(vector)
    res = prod(map(factorial, hist.values()))
    return res

class multinomial_events:
    def __init__(self, n = None, probs = None):
        self.trials = self.n = n
        self.k = len(probs)
        self.probs = probs
        self.expected_freqs = np.round(np.array(self.probs) * self.n)
    def init_using_expected_freqs(self, expected_freqs):
        self.trials = self.n = len(expected_freqs)
        self.probs = np.array(expected_freqs) / self.trials
        self.k = len(self.probs)
        self.expected_freqs = expected_freqs
    def event_id(self, outcome):
        return int(chi2_stat_as_int(outcome, self.expected_freqs))
    def outcome2statistic(self, outcome):
        return scipy.stats.chisquare(outcome, self.expected_freqs).statistic

    def outcomes_gen(self, unique_perms = True):
        for outcome in subset_sum(subset_size = self.k,
                                target_sum = self.n, Set=range(self.n+1), unique_perms=unique_perms):
            if unique_perms:
                yield outcome
            else:
                for outcome_perm in set(permutations(outcome)):
                    yield outcome_perm
    def event_prob(self, event_outcomes):
        prob = 0
        for outcome in event_outcomes:
            num_outcome_perms = num_equivalent_perms(vector=outcome)
            scipy_prob = scipy.stats.multinomial.pmf(outcome, self.n, self.probs)
            prob += scipy_prob * math.factorial(self.k) / num_outcome_perms
            # print(outcome, scipy_prob, num_outcome_perms, prob)
        return prob
    def events_data(self):
        self.event_outcomes = defaultdict(list)
        self.event_stats = {}
        self.event_pmf = defaultdict(int)

        #outcomes grouped - unique outcomes (permutations of outcomes are not repeated)
        for outcome in self.outcomes_gen(unique_perms = True):
            event_id = self.event_id(outcome)
            self.event_outcomes[event_id].append(outcome)

        # stat computed for each group of outcomes
        self.event_stats = {}
        for event_id in self.event_outcomes:
            outcomes = self.event_outcomes[event_id]
            stat = self.outcome2statistic(outcomes[0])
            self.event_stats[event_id] = stat

        # pmf (probability) computed for each group
        for event_id, outcomes in self.event_outcomes.items():
            self.event_pmf[event_id] += self.event_prob(outcomes)

        #sorted according statistics
        stats_sorted = dict(sorted(self.event_stats.items(), key=lambda x: x[1]))

        self.dist = {}
        self.dist['events_stat'] = [self.event_stats[event_id] for event_id in stats_sorted]
        self.dist['events_pmf'] = [self.event_pmf[event_id] for event_id in stats_sorted]
        self.dist['less'] = np.cumsum(self.dist['events_pmf'])
        self.dist['greater'] = np.array([1] * len(self.dist['less'])) - self.dist['less']
        self.dist['two-sided'] = 2 * np.minimum(self.dist['less'], self.dist['greater'])

    def pmf(self, outcome):
        if isinstance(outcome, int):
            event_id = outcome
        if isinstance(outcome, list):
            event_id = self.event_id_func(outcome)
        assert 'pdf' in self.dist and  event_id in self.dist['pdf']
        return self.dist['pdf'][event_id]

    def cdf(self, outcome):
        if isinstance(outcome, int):
            event_id = outcome
        if isinstance(outcome, list):
            event_id = self.event_id_func(outcome)
        assert 'less' in self.dist and  event_id in self.dist['less']
        return self.dist['less'][event_id]

if __name__ == '__main__':
    M = multinomial_events(n = 6, probs = [1/3]*3)
    M.events_data()
    print(sum(M.dist['events_pmf']))
    print(M.dist['less'])
    print(M.dist['event_stat'])
    print(M.event_outcomes)
