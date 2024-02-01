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


def output_file(freq_it, batch_n):
    filename = f'frequent_itemsets_netflix2%_{batch_n}.txt'
    with open(filename, 'w') as file:
        for itemset, support in freq_it.items():
            file.write(f"{', '.join(itemset)}: {support:.2%}\n")


def file_load(file):
    with open(file, 'r') as file:
        d = []
        for line in file:
            transaction = line.strip().split()
            d.append(transaction)
    return d


file_1 = "netflix.data"
data = file_load(file_1)
min_support = 0.02
batch_size = 3000
save_interval = 700

start_time = time.time()
last_save_time = start_time
freq_pair = {}

batch_number = 1
count_f = 0

for i in range(0, len(data), batch_size):
    batch = data[i:i + batch_size]
    pruned_2_item_candidates = apriori(batch, 2, min_support)
    count_f += len(pruned_2_item_candidates)
    freq_pair.update(pruned_2_item_candidates)

    current_time = time.time()
    elapsed_time = current_time - start_time

    if current_time - last_save_time >= save_interval:
        output_file(freq_pair, batch_number)
        last_save_time = current_time
        batch_number += 1

end_time = time.time()
elapsed_time = end_time - start_time

output_file(freq_pair, batch_number)

print("Frequent 2-Item Pairs and Their Support:")
print(count_f)
print("Time Elapsed: {:.2f} seconds".format(elapsed_time))
