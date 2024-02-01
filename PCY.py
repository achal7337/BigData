import time
from itertools import combinations
from collections import Counter


def candidate_gen(sets, size):
    cand = []
    for s in sets:
        cand.extend(combinations(s, size))
    return cand


def apriori(sets, k, sup_min):
    total_counts = len(sets)

    candidates = candidate_gen(sets, k)

    candidate_counts = Counter(candidates)

    support_c = {}
    for candidate, count in candidate_counts.items():
        support_c[candidate] = count / total_counts

    generated_can = {candidate: support_c for candidate, support_c in support_c.items() if support_c >= sup_min}

    return generated_can


def pcy_algorithm(data, minimum_Sup, size_hash):

    hash_table = [0] * size_hash

    cand_it = apriori(data, 2, minimum_Sup)

    for item_sets in data:
        for item1, item2 in combinations(item_sets, 2):
            if (item1, item2) in cand_it:
                bucket = hash((item1, item2)) % size_hash
                hash_table[bucket] += 1

    freq_items = set()
    for item1, item2 in cand_it:
        bucket = hash((item1, item2)) % size_hash
        if hash_table[bucket] >= minimum_Sup:
            freq_items.add((item1, item2))

    return freq_items


def file_load(file):
    with open(file, 'r') as file:
        d = []
        for line in file:
            transaction = line.strip().split()
            d.append(transaction)
    return d


file_name = "retail.dat.txt"
file_1 = file_load(file_name)

min_support = 0.01

hash_bucket_size = 10

start_time = time.time()
freq_pair = pcy_algorithm(file_1, min_support, hash_bucket_size)
end_time = time.time()
elapsed_time = end_time - start_time
min_support1 = 0.02
outputfile = "frequentitemset_pcy1.txt"
count_f = len(freq_pair)
freq_pair1 = pcy_algorithm(file_1, min_support1, hash_bucket_size)
count_f1 = len(freq_pair1)
with open(outputfile, 'w') as file:
    file.write(f"Total Frequent 2-Item Pairs for 1%: {count_f}\n")
    for itemset in freq_pair:
        file.write(f"{', '.join(map(str, itemset))}\n")
    file.write(f"\n\nTotal Frequent 2-Item Pairs for 2%: {count_f1}\n")
    for itemset in freq_pair1:
        file.write(f"{', '.join(map(str, itemset))}\n")


print("Time Elapsed: {:.2f} seconds".format(elapsed_time))
