from ctypes import *


libpvals = CDLL('../C/libpvals.so')

# utils.c - field of second level uniformity tests (from batteries mostly)
# GoF_functions[] = { & dieharder_pvalue, & dieharder_pvalue_kuiper, & nist_pvalue, & testu01_pvalue_snpair_ClosePairs, & testu01_pvalue_sknuth_MaxOft,
# & testu01_pvalue_ksp, & testu01_pvalue_ksm, & testu01_pvalue_ks, & testu01_pvalue_ad, & testu01_pvalue_cm, & testu01_pvalue_wg,
# & testu01_pvalue_wu, & KS_left, & KS_right, & KS_both, & dieharder_corrected_pvalue};

GoF_test_names = {0:"dieharder_pvalue", 1:"dieharder_pvalue_kuiper", 2:"nist_pvalue", 3:"testu01_pvalue_snpair_ClosePairs",
       4:"testu01_pvalue_sknuth_MaxOft", 5:"testu01_pvalue_ksp", 6:"testu01_pvalue_ksm", 7:"testu01_pvalue_ks",
       8:"testu01_pvalue_ad", 9:"testu01_pvalue_cm", 10:"testu01_pvalue_wg", 11:"testu01_pvalue_wu",
        12:"KS_left", 13:"KS_right", 14:"KS_both", 15:"dieharder_corrected_pvalue"}


# C: prototype GoF_pvals(const char* src_file, int sample_size, int repetitions, int GoF_idx, double* resulted_pvals)
def GoF_pvals_wrapper(pvals_filepath, sample_size, GoF_idx, repetitions):
    libpvals.GoF_pvals.argtypes = [c_char_p, c_int, c_int, c_int, POINTER(c_double)]
    libpvals.GoF_pvals.restype = None

    array = [-1] * repetitions
    resulted_pvals = (c_double * repetitions)(*array)

    libpvals.GoF_pvals(pvals_filepath.encode(), c_int(sample_size), c_int(repetitions), c_int(GoF_idx), resulted_pvals)
    return GoF_test_names[GoF_idx], list(resulted_pvals)


if __name__ == "__main__":
    GoF_pvals = GoF_pvals_wrapper("../../data/uniform_pvals_devurand.pval", 100, 0, 100000)
