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


def multistage_pcy(data, minimum_sup, bucket_size, stages_num):
    hash_tables = [dict() for _ in range(stages_num)]

    cand_it = apriori(data, 2, minimum_sup)

    for stage in range(stages_num):
        hash_bucket_size = bucket_size[stage]
        hash_table = hash_tables[stage]

        for item_sets in data:
            for item1, item2 in combinations(item_sets, 2):
                if (item1, item2) in cand_it:
                    bucket = hash((item1, item2)) % hash_bucket_size
                    if bucket in hash_table:
                        hash_table[bucket] += 1
                    else:
                        hash_table[bucket] = 1

    freq = set()

    for item1, item2 in cand_it:
        passed_all_stages = all(
            (hash((item1, item2)) % bucket_size[stage]) in hash_tables[stage]
            for stage in range(stages_num)
        )
        if passed_all_stages:
            freq.add((item1, item2))

    return freq


def file_load(file):
    with open(file, 'r') as file:
        d = []
        for line in file:
            transaction = line.strip().split()
            d.append(transaction)
    return d


def output_file(output, file_n, total_f):
    with open(file_n, 'w') as file:
        file.write(f"total Frequent Pairs: {total_f}\n")
        for j in output:
            file.write(f"{','.join(map(str, j))}\n")


file_1 = "retail.dat.txt"
data = file_load(file_1)
min_support = 0.01
min_support1 = 0.02  # Adjust the minimum support as needed
hash_bucket_sizes = [10000, 5000, 2000]  # Adjust the hash bucket sizes for each stage
num_stages = len(hash_bucket_sizes)
outputfile = "frequentitemset_multi.txt"
start_time = time.time()
freq_pair = multistage_pcy(data, min_support, hash_bucket_sizes, num_stages)
count_f = len(freq_pair)
freq_pair1 = multistage_pcy(data, min_support1, hash_bucket_sizes, num_stages)
count_f1 = len(freq_pair1)
end_time = time.time()
elapsed_time = end_time - start_time

with open(outputfile, 'w') as file:
    file.write(f"Total Frequent 2-Item Pairs for 1%: {count_f}\n")
    for itemset in freq_pair:
        file.write(f"{', '.join(map(str, itemset))}\n")
    file.write(f"\n\nTotal Frequent 2-Item Pairs for 2%: {count_f1}\n")
    for itemset in freq_pair1:
        file.write(f"{', '.join(map(str, itemset))}\n")


print("Time Elapsed: {:.2f} seconds".format(elapsed_time))