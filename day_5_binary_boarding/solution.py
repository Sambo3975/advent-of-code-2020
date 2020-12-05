def deduce_location(pass_code, lower, upper):
    if lower == upper:
        return lower

    half = pass_code[0]
    middle = lower + (upper - lower) // 2
    if half in ['F', 'L']:
        return deduce_location(pass_code[1:], lower, middle)
    if half in ['B', 'R']:
        return deduce_location(pass_code[1:], middle + 1, upper)


def deduce_row(pass_code):
    return deduce_location(pass_code, 0, 127)


def deduce_column(pass_code):
    return deduce_location(pass_code, 0, 7)


def decode_pass(pass_code):
    row_id = deduce_row(pass_code[:-3])
    column_id = deduce_column(pass_code[-3:])
    return row_id * 8 + column_id


def parse_input(file_name):
    with open(file_name) as f:
        return [line[:-1] for line in f.readlines()]


if __name__ == '__main__':
    passes = parse_input('input.txt')

    taken_seats = []  # For part 2

    # Part 1: Highest Seat ID
    highest_id = 0
    for code in passes:
        pass_id = decode_pass(code)
        highest_id = max(highest_id, pass_id)
        taken_seats.append(pass_id)
    print('highest ID: {}'.format(highest_id))

    # Part 2: Where's my seat?
    taken_seats.sort()
    previous_id = taken_seats[0]
    for x in taken_seats:
        if previous_id == x - 2:  # Found the one-seat gap
            print('My seat ID: {}'.format(previous_id + 1))
            break
        previous_id = x
