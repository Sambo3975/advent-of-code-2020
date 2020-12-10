def read_ints(file_name):
    """Read a file, line by line, as a list of integers"""
    ints = []
    with open(file_name) as f:
        for line in f.readlines():
            ints.append(int(line))
    return ints


def sum_2020(report):
    length = len(report)
    for i in range(length - 1):
        for j in range(i, length):
            if report[i] + report[j] == 2020:
                return report[i] * report[j]


def sum_2020_redux(report):
    length = len(report)
    for i in range(length - 2):
        for j in range(i, length - 1):
            for k in range(j, length):
                if report[i] + report[j] + report[k] == 2020:
                    return report[i] * report[j] * report[k]


if __name__ == '__main__':
    problem_input = read_ints('input.txt')
    product = sum_2020(problem_input)
    print('Product 1: {}'.format(product))
    product = sum_2020_redux(problem_input)
    print('Product 2: {}'.format(product))
