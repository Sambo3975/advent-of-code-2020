def read_input(file_name):
    data = []
    with open(file_name) as f:
        for line in f.readlines():
            data.append(line[:-1])  # trim the \n characters
    return data


def count_trees_in_path(data, over, down):
    max_x = len(data[0])
    max_y = len(data)
    x = 0
    y = 0
    trees = 0
    while y < max_y:
        if data[y][x] == '#':
            trees += 1
        x = (x + over) % max_x
        y += down
    return trees


slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]


def part_2(data):
    product = 1
    for pair in slopes:
        tree_ct = count_trees_in_path(data, pair[0], pair[1])
        product *= tree_ct
    return product


if __name__ == '__main__':
    tree_data = read_input('input.txt')
    tree_count = count_trees_in_path(tree_data, 3, 1)
    print('Trees encountered: {}'.format(tree_count))

    tree_product = part_2(tree_data)
    print('Product of tree counts on all slopes: {}'.format(tree_product))
