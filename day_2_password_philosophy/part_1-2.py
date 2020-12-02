def parse_line(line):
    parts = line.split(' ')
    counts = parts[0].split('-')
    letter = parts[1][0]
    return int(counts[0]), int(counts[1]), letter, parts[2]


def check_passwords_1(file_name):
    valid_count = 0
    with open(file_name) as f:
        for line in f.readlines():
            min_count, max_count, letter, password = parse_line(line)
            count = 0
            for char in password:
                if char == letter:
                    count += 1
            if min_count <= count <= max_count:
                valid_count += 1
    return valid_count


def xor(cond_1, cond_2):
    return (cond_1 and not cond_2) or (cond_2 and not cond_1)


def check_passwords_2(file_name):
    valid_count = 0
    with open(file_name) as f:
        for line in f.readlines():
            pos_1, pos_2, letter, password = parse_line(line)
            if xor(password[pos_1 - 1] == letter, password[pos_2 - 1] == letter):
                valid_count += 1
    return valid_count


if __name__ == '__main__':
    print('Valid password count 1: {}'.format(check_passwords_1('input.txt')))
    print('Valid password count 2: {}'.format(check_passwords_2('input.txt')))
