from math import ceil
from numpy import array, argsort


def parse_file_no_x(file_name):
    with open(file_name) as f:
        data = f.readlines()
    return int(data[0]), [int(x) for x in data[1].replace('x,', '').split(',')]


def parse_file_with_x(file_name):
    with open(file_name) as f:
        data = f.readlines()[1].split(',')

    n = []  # moduli
    a = []  # remainders
    for i in range(len(data)):
        if data[i] != 'x':
            n.append(int(data[i]))
            a.append(int(i))

    array_n = array(n)
    sort_indices = argsort(array_n)[::-1]
    return [n[x] for x in sort_indices], [(n[x] - a[x]) % n[x] for x in sort_indices]


def get_earliest_departure(earliest, ids):
    earliest_id = 0
    shortest_wait = max(ids)
    for x in ids:
        wait = (ceil(earliest / x) * x) % earliest
        if wait < shortest_wait:
            earliest_id = x
            shortest_wait = wait
    return earliest_id, shortest_wait


def solve_modular_congruency_system(n, a):
    """See the Wikipedia article on the Chinese Remainder Theorem. This is an implementation of the sieving method as
    described there. This has exponential complexity but is good enough in this case as we aren't working with large
    primes. """
    step = 1
    x = a[0]
    for i in range(len(a) - 1):
        step *= n[i]
        while x % n[i + 1] != a[i + 1]:
            x += step
    return x


if __name__ == '__main__':
    earliest_departure, bus_ids = parse_file_no_x('input.txt')
    bus_id, wait_time = get_earliest_departure(earliest_departure, bus_ids)
    print(f"Bus ID with the shortest wait: {bus_id} ({wait_time} minutes)\nProduct: {bus_id * wait_time}")
    moduli, remainders = parse_file_with_x('input.txt')
    timestamp = solve_modular_congruency_system(moduli, remainders)
    print(f"\nEarliest timestamp with desired departure pattern: {timestamp}")
