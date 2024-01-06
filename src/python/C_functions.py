from ctypes import *
import utils

libpvals = CDLL('../C/libpvals.so')

# utils.c - field of second level uniformity tests (from batteries mostly)
# GoF_functions[] = { & dieharder_pvalue, & dieharder_pvalue_kuiper, & nist_pvalue, & testu01_pvalue_snpair_ClosePairs, & testu01_pvalue_sknuth_MaxOft,
# & testu01_pvalue_ksp, & testu01_pvalue_ksm, & testu01_pvalue_ks, & testu01_pvalue_ad, & testu01_pvalue_cm, & testu01_pvalue_wg,
# & testu01_pvalue_wu, & KS_left, & KS_right, & KS_both, & dieharder_corrected_pvalue};

GoF_test_names = {0:"dieharder_pvalue", 1:"dieharder_pvalue_kuiper", 2:"nist_pvalue", 3:"testu01_pvalue_snpair_ClosePairs",
       4:"testu01_pvalue_sknuth_MaxOft", 5:"testu01_pvalue_ksp", 6:"testu01_pvalue_ksm", 7:"testu01_pvalue_ks",
       8:"testu01_pvalue_ad", 9:"testu01_pvalue_cm", 10:"testu01_pvalue_wg", 11:"testu01_pvalue_wu",
        12:"marsa_KS_left_pvalue", 13:"marsa_KS_right_pvalue", 14:"marsa_both_pvalue", 15:"dieharder_corrected_pvalue",
        16:"dieharder_fast_pvalue"}


# C: prototype GoF_pvals(const char* src_file, int sample_size, int repetitions, int GoF_idx, double* resulted_pvals)
def GoF_pvals_wrapper(pvals_filepath, sample_size, GoF_idx, repetitions, seed):
    libpvals.GoF_pvals.argtypes = [c_char_p, c_int, c_int, c_int, POINTER(c_double), c_int]
    libpvals.GoF_pvals.restype = None

    array = [-1] * repetitions
    resulted_pvals = (c_double * repetitions)(*array)

    libpvals.GoF_pvals(pvals_filepath.encode(), c_int(sample_size), c_int(repetitions), c_int(GoF_idx), resulted_pvals, seed)
    return GoF_test_names[GoF_idx], list(resulted_pvals)

################################### GoFs from batteries plus some alternative ####################################

def dieharder_pvalue(pvals, num_pvals):
    libpvals.dieharder_pvalue.argtypes = [POINTER(c_double), c_int]
    libpvals.dieharder_pvalue.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.dieharder_pvalue(array, num_pvals)

def dieharder_pvalue_kuiper(pvals, num_pvals):
    libpvals.dieharder_pvalue_kuiper.argtypes = [POINTER(c_double), c_int]
    libpvals.dieharder_pvalue_kuiper.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.dieharder_pvalue_kuiper(array, num_pvals)

def nist_pvalue(pvals, num_pvals):
    libpvals.nist_pvalue.argtypes = [POINTER(c_double), c_int]
    libpvals.nist_pvalue.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.nist_pvalue(array, num_pvals)

def testu01_pvalue_snpair_ClosePairs(pvals, num_pvals):
    libpvals.testu01_pvalue_snpair_ClosePairs.argtypes = [POINTER(c_double), c_int]
    libpvals.testu01_pvalue_snpair_ClosePairs.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.testu01_pvalue_snpair_ClosePairs(array, num_pvals)

def testu01_pvalue_sknuth_MaxOft(pvals, num_pvals):
    libpvals.testu01_pvalue_sknuth_MaxOft.argtypes = [POINTER(c_double), c_int]
    libpvals.testu01_pvalue_sknuth_MaxOft.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.testu01_pvalue_sknuth_MaxOft(array, num_pvals)

def testu01_pvalue_ksp(pvals, num_pvals):
    libpvals.testu01_pvalue_ksp.argtypes = [POINTER(c_double), c_int]
    libpvals.testu01_pvalue_ksp.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.testu01_pvalue_ksp(array, num_pvals)

def testu01_pvalue_ksm(pvals, num_pvals):
    libpvals.testu01_pvalue_ksm.argtypes = [POINTER(c_double), c_int]
    libpvals.testu01_pvalue_ksm.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.testu01_pvalue_ksm(array, num_pvals)

def testu01_pvalue_ks(pvals, num_pvals):
    libpvals.testu01_pvalue_ks.argtypes = [POINTER(c_double), c_int]
    libpvals.testu01_pvalue_ks.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.testu01_pvalue_ks(array, num_pvals)

def testu01_pvalue_ad(pvals, num_pvals):
    libpvals.testu01_pvalue_ad.argtypes = [POINTER(c_double), c_int]
    libpvals.testu01_pvalue_ad.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.testu01_pvalue_ad(array, num_pvals)

def testu01_pvalue_cm(pvals, num_pvals):
    libpvals.testu01_pvalue_cm.argtypes = [POINTER(c_double), c_int]
    libpvals.testu01_pvalue_cm.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.testu01_pvalue_cm(array, num_pvals)

def testu01_pvalue_wg(pvals, num_pvals):
    libpvals.testu01_pvalue_wg.argtypes = [POINTER(c_double), c_int]
    libpvals.testu01_pvalue_wg.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.testu01_pvalue_wg(array, num_pvals)

def testu01_pvalue_wu(pvals, num_pvals):
    libpvals.testu01_pvalue_wu.argtypes = [POINTER(c_double), c_int]
    libpvals.testu01_pvalue_wu.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.testu01_pvalue_wu(array, num_pvals)

def marsa_KS_left_pvalue(pvals, num_pvals):
    libpvals.marsa_KS_left_pvalue.argtypes = [POINTER(c_double), c_int]
    libpvals.marsa_KS_left_pvalue.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.marsa_KS_left_pvalue(array, num_pvals)

def marsa_KS_right_pvalue(pvals, num_pvals):
    libpvals.marsa_KS_right_pvalue.argtypes = [POINTER(c_double), c_int]
    libpvals.marsa_KS_right_pvalue.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.marsa_KS_right_pvalue(array, num_pvals)

def marsa_KS_both_pvalue(pvals, num_pvals):
    libpvals.marsa_KS_both_pvalue.argtypes = [POINTER(c_double), c_int]
    libpvals.marsa_KS_both_pvalue.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.marsa_KS_both_pvalue(array, num_pvals)

def dieharder_corrected_pvalue(pvals, num_pvals):
    libpvals.dieharder_corrected_pvalue.argtypes = [POINTER(c_double), c_int]
    libpvals.dieharder_corrected_pvalue.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.dieharder_corrected_pvalue(array, num_pvals)

def dieharder_fast_pvalue(pvals, num_pvals):
    libpvals.dieharder_fast_pvalue.argtypes = [POINTER(c_double), c_int]
    libpvals.dieharder_fast_pvalue.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.dieharder_fast_pvalue(array, num_pvals)


################################### Marsaglia funcs ####################################

def KS_cdf(stat, num_pvals):
    libpvals.K.argtypes = [c_int, c_double]
    libpvals.K.restype = c_double
    return libpvals.K(num_pvals, stat)

def KS_left_pvalue(pvals, num_pvals):
    libpvals.KS_left_pvalue.argtypes = [POINTER(c_double), c_int]
    libpvals.KS_left_pvalue.restype = c_double
    array = (c_double * num_pvals)(*pvals)
    return libpvals.KS_left_pvalue(array, num_pvals)

if __name__ == "__main__":
    pvals = utils.uniform_random(1000) + 0.07
    # GoF_pvals = GoF_pvals_wrapper("../../data/uniform_pvals_devurand.pval", 100, 0, 100000)
    print(marsa_KS_right_pvalue(pvals, len(pvals)))
    print(dieharder_pvalue(pvals, len(pvals)))
    print(dieharder_fast_pvalue(pvals, len(pvals)))
    print(utils.KS_test_scipy(pvals))
