import time
from itertools import combinations
from collections import Counter

start_time = time.time()


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


def file_load(file):
    with open(file, 'r') as file:
        d = []
        for line in file:
            transaction = line.strip().split()
            d.append(transaction)
    return d


file_name = "retail.dat.txt"
file_1 = file_load(file_name)
# minimum support
min_support = 0.01


def output_file(output, file_n, total_f):
    with open(file_n, 'w') as file:
        file.write(f"total Frequent Pairs: {total_f}\n")
        for j, sup in output.items():
            file.write(f"{','.join(map(str, j))}:{sup:.2%}\n")


end_time = time.time()
elapsed_time = end_time - start_time
# Generating freq item set
min_support1 = 0.02
freq_pair = apriori(file_1, 2, min_support)
outputfile = "frequentitemset_apriori.txt"
count_f = len(freq_pair)
freq_pair1 = apriori(file_1, 2, min_support1)
count_f1 = len(freq_pair1)

with open(outputfile, 'w') as file:
    file.write(f"Total Frequent 2-Item Pairs for 1%: {count_f}\n")
    for itemset in freq_pair:
        file.write(f"{', '.join(map(str, itemset))}\n")
    file.write(f"\n\nTotal Frequent 2-Item Pairs for 2%: {count_f1}\n")
    for itemset in freq_pair1:
        file.write(f"{', '.join(map(str, itemset))}\n")

print("Time Elapsed: {:.2f} seconds".format(elapsed_time))
