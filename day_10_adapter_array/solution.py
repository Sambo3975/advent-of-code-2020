from collections import Counter


def read_ints(file_name):
    """Read a file, line by line, as a list of integers"""
    with open(file_name) as f:
        return [int(x) for x in f.readlines()]


def get_joltage_change_distribution(adapters):
    adapters.sort()
    changes = [adapters[0]]  # outlet -> first adapter: 1 or 3
    for i in range(len(adapters) - 1):
        changes.append(adapters[i + 1] - adapters[i])
    changes.append(3)  # last adapter -> device: always 3
    c = Counter(changes)
    return c


def list_removable(adapters):
    ls = []
    if adapters[0] == 1:
        ls.append(1)
    for i in range(1, len(adapters) - 1):
        if adapters[i] - adapters[i - 1] == 1 and adapters[i + 1] - adapters[i] == 1:
            ls.append(adapters[i])
    return ls


options_by_run_size = [
    1,  # 0 choose 0 (1) -- not that there's a point in including this one
    2,  # 1 choose 1 (1) + 1 choose 0 (1)
    4,  # 2 choose 2 (1) + 2 choose 1 (2) + 2 choose 0 (1)
    7,  # 3 choose 2 (3) + 3 choose 1 (3) + 3 choose 0 (1)
]


def count_possibilities(remove_list):
    possibilities = 1
    start = 0
    end = 0
    while end < len(remove_list):
        while remove_list[end] - remove_list[start] < 3:
            end += 1
            if end == len(remove_list):
                break
        possibilities *= options_by_run_size[end - start]
        start = end
    return possibilities


if __name__ == '__main__':
    adapter_list = read_ints('input.txt')
    counter = get_joltage_change_distribution(adapter_list)
    encoded = counter[1] * counter[3]
    print(f"Differences of 1: {counter[1]}. Differences of 2: {counter[3]}.\nProduct: {encoded}.")
    rm_list = list_removable(adapter_list)
    possibility_count = count_possibilities(rm_list)
    print(f"There are {possibility_count} options to choose from. I'd recommend the one with the fewest adapters.")
