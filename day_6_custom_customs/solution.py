def read_input(file_name):
    with open(file_name) as f:
        return f.read().split('\n\n')


answers = {}
for i in range(ord('a'), ord('z') + 1):
    answers[chr(i)] = 0


def reset_answer_table():
    global answers
    for k in answers:
        answers[k] = 0


def read_answers_group(entry, require_unanimous):
    reset_answer_table()

    global answers

    responses = entry.split()
    for a in responses:
        for char in a:
            answers[char] += 1

    yes_count = 0
    for k in answers:
        if (not require_unanimous and answers[k] > 0) or answers[k] == len(responses):
            yes_count += 1
    return yes_count


def read_all_answers(entries, require_unanimous=False):
    yes_count = 0
    for e in entries:
        yes_count += read_answers_group(e, require_unanimous)
    return yes_count


if __name__ == '__main__':
    inputs = read_input('input.txt')

    yes_total = read_all_answers(inputs)
    print('Yes count: {}'.format(yes_total))

    yes_total = read_all_answers(inputs, True)
    print('Unanimous yes count: {}'.format(yes_total))
