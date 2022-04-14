import sys
import numpy as np
from decimal import Decimal, ROUND_HALF_UP


def standardize_matrix(matrix):
    stnd_matrix = []
    for row in matrix:
        mean_value = np.nanmean(row)
        stnd_row = list(map(lambda i: 0 if np.isnan(i) else (i - mean_value), row))
        stnd_matrix.append(stnd_row)
    return np.array(stnd_matrix)


def cf_query(matrix, stnd_matrix, i, j, k):
    # pearson
    pearson_list = []
    for row in stnd_matrix:
        pval = np.corrcoef(stnd_matrix[i], row)[0][1]
        if pval < 0:
            pearson_list.append(0)
        else:
            pearson_list.append(pval)
    pearson_list[i] = 0

    for ln, row in enumerate(matrix):
        if np.isnan(row[j]):
            pearson_list[ln] = 0

    np_pearson_k = np.array(sorted(pearson_list)[-k:])
    np_pearson_clean_k = np_pearson_k[np_pearson_k > 0]
    numerator, denominator = 0, 0
    for p in np_pearson_clean_k:
        row_index = pearson_list.index(p)
        numerator += p * matrix[row_index][j]
        denominator += p

    return numerator / denominator


def main():
    """ Reading inputs and execution """
    # load matrix
    matrix_size = sys.stdin.readline().strip().split()
    N = int(matrix_size[0])
    M = int(matrix_size[1])
    matrix = []
    for _ in range(N):
        matrix_row = sys.stdin.readline().strip().split()
        clean_row = list(map(lambda i: None if i == "X" else i, matrix_row))
        matrix.append(clean_row)
    np_matrix = np.array(matrix, dtype=np.float64)

    # prepare matrixes
    np_item_item_matrix = np_matrix
    np_item_item_stnd_matrix = standardize_matrix(np_matrix)  # for T = 0
    np_user_user_matrix = np_matrix.transpose()
    np_user_user_stnd_matrix = standardize_matrix(np_user_user_matrix)  # for T = 1

    # execute queries
    Q = int(sys.stdin.readline().strip())
    for _ in range(Q):
        ijtk_line = sys.stdin.readline().strip().split()
        i, j, t, k = list(map(lambda i: int(i), ijtk_line))
        if t:
            result = cf_query(np_user_user_matrix, np_user_user_stnd_matrix, j-1, i-1, k)
        else:
            result = cf_query(np_item_item_matrix, np_item_item_stnd_matrix, i-1, j-1, k)
        rresult = Decimal(Decimal(result).quantize(Decimal('.001'), rounding=ROUND_HALF_UP))
        print(rresult)


if __name__ == "__main__":
    main()
