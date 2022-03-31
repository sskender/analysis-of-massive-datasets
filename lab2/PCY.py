import sys
import math


def pcy(basket_num, bucket_num, threshold, basket_list):
    """ PCY algorithm """
    # first pass
    items_count = {}
    for basket in basket_list:
        for item in basket:
            items_count[item] = items_count.get(item, 0) + 1

    # second pass
    buckets = {}
    for basket in basket_list:
        for i in range(0, len(basket) - 1):
            for j in range(i + 1, len(basket)):
                item_i = basket[i]
                item_j = basket[j]
                if items_count[item_i] >= threshold and items_count[item_j] >= threshold:
                    k = ((item_i * len(items_count)) + item_j) % bucket_num
                    buckets[k] = buckets.get(k, 0) + 1

    # third pass
    pairs = {}
    for basket in basket_list:
        for i in range(0, len(basket) - 1):
            for j in range(i + 1, len(basket)):
                item_i = basket[i]
                item_j = basket[j]
                if items_count[item_i] >= threshold and items_count[item_j] >= threshold:
                    k = ((item_i * len(items_count)) + item_j) % bucket_num
                    if buckets[k] >= threshold:
                        key = (item_i, item_j)
                        pairs[key] = pairs.get(key, 0) + 1

    return items_count, buckets, pairs


def main():
    """" main """
    # input
    N = int(sys.stdin.readline().strip())
    s = float(sys.stdin.readline().strip())
    b = int(sys.stdin.readline().strip())
    baskets_input = sys.stdin.read().strip().split("\n")
    threshold = math.floor(N * s)
    baskets_list = []
    for _, basket in enumerate(baskets_input):
        baskets_list.append([int(article) for article in basket.split()])

    # pcy algo
    items_dict, _, pairs_dict = pcy(N, b, threshold, baskets_list)

    # output
    m = len(items_dict)
    print((m * (m - 1)) // 2)
    print(len(pairs_dict))
    for key in sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True):
        print(key[1])


if __name__ == "__main__":
    main()
