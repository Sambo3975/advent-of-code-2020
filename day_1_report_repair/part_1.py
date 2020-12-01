from utils import Utils


def sum_2020(report):
    length = len(report)
    for i in range(length - 1):
        for j in range(i, length):
            if report[i] + report[j] == 2020:
                return report[i] * report[j]


if __name__ == '__main__':
    problem_input = Utils.read_ints('input.txt')
    product = sum_2020(problem_input)
    print('Product: {}'.format(product))
