import threading

number_positions = None
next_position = 0
previous_number = 0


def parse_file(file_name):
    global number_positions, next_position, previous_number
    with open(file_name) as f:
        data = f.read().split(',')
    number_positions = {}
    for i in range(len(data) - 1):
        number_positions[int(data[i])] = i
    next_position = len(data) - 1
    previous_number = int(data[-1])


def get_next_number():
    global number_positions, next_position, previous_number

    if previous_number in number_positions:
        next_number = next_position - number_positions[previous_number]
    else:
        next_number = 0

    number_positions[previous_number] = next_position

    previous_number = next_number
    next_position += 1


def thread_get_nth_number(file_name, n):
    parse_file(file_name)
    while next_position + 1 < n:
        get_next_number()


if __name__ == '__main__':
    load_sequence = "-\\|/"
    current_sequence_pos = 0
    for x in [2020, 30000000]:
        print(f"{x}th number: /", end='')
        thread = threading.Thread(target=thread_get_nth_number, args=('input.txt', x))
        thread.start()
        while thread.is_alive():
            print(f"\b{load_sequence[current_sequence_pos]}", end='')
            current_sequence_pos = (current_sequence_pos + 1) % len(load_sequence)
            thread.join(.005)
        print(f"\b{previous_number}")
