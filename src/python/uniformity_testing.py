from C_functions import GoF_pvals_wrapper, GoF_test_names
import json
import  collections
import matplotlib.pyplot as plt
import numpy as np
import time
from utils import histogram

def GoF_uniformity_data():
    res = collections.defaultdict(dict)
    for sample_size in [10, 100, 1000, 10000]:
        for test_idx in range(2, len(GoF_test_names)):
            start = time.time()
            GoF_test_name, pvals = GoF_pvals_wrapper(pvals_filename="../../data/uniform_pvals_devurand.pval",
                                                     sample_size=sample_size, GoF_idx=test_idx, repetitions=100000)
            end = time.time()
            res[GoF_test_name][sample_size] = pvals
            print(GoF_test_name, sample_size, end - start)
            json.dump(res, open("../../data/GoF_uniformity.json", "w"))
# GoF_uniformity_data()

def merge_parts():
    GoF_uniformity_1 = json.load(open("../../data/GoF_uniformity_1st_part.json"))
    GoF_uniformity_2 = json.load(open("../../data/GoF_uniformity_2nd_part.json"))
    for size in GoF_uniformity_2:
        for test in GoF_uniformity_2[size]:
            GoF_uniformity_1[size][test] = GoF_uniformity_2[size][test]
    json.dump(GoF_uniformity_1, open("../../data/GoF_uniformity.json", "w"))
# merge_parts()

def plot_histogram(freqs, size, data_src, params, filename=None):
    plt.bar(np.arange(len(freqs)) + 1, freqs)
    plt.title(f"Histogram: src={data_src}\n params={params}")
    plt.xlabel('p-values')
    plt.ylabel('Frequency')
    if filename != None:
        plt.savefig(filename)
    plt.close()
def Gof_histograms():
    GoF_uniformity = json.load(open("../../data/GoF_uniformity.json"))
    for num_bins in [10, 100, 1000]:
        for test in GoF_uniformity.keys():
            for size in GoF_uniformity[test]:
                pvals = GoF_uniformity[test][size]
                size = int(size)
                step = 1 / num_bins
                bin_edges = np.arange(num_bins+2)*step
                freqs = list(histogram(bin_edges, pvals).values())
                print(f"test={test}, size={size} x<0 freq={freqs[0]}, x>1 freq={freqs[-1]}")
                freqs = freqs[1:-1]
                plot_histogram(freqs, size, test, params = f"Sample size={size}",
                filename=f"../../data/images/GoF_uniformity_bins_{num_bins}/{test}_{size}_GoFUniHist.png")

Gof_histograms()