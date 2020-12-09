class CircularBuffer:
    """Simple circular buffer"""

    def __init__(self, data=None, capacity=None):
        if data is None:
            data = []
        if capacity is None:
            capacity = len(data)

        self.__data = data
        self.__capacity = capacity
        self.__current_position = 0
        self.__iter = 0

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, item):
        if len(self.__data) < self.__capacity:
            return self.__data[item]
        else:
            return self.__data[(self.__current_position + item) % len(self.__data)]

    def __iter__(self):
        self.__iter = 0
        return self

    def __next__(self):
        if self.__iter < len(self.__data):
            x = self[self.__iter]
            self.__iter += 1
            return x
        else:
            raise StopIteration

    def capacity(self):
        return self.__capacity

    def append(self, item):
        if len(self.__data) < self.__capacity:
            self.__data.append(item)
        else:
            self.__data[self.__current_position] = item
        self.__current_position = (self.__current_position + 1) % self.__capacity


def parse_input(file_name):
    with open(file_name) as f:
        return [int(x) for x in f.readlines()]


def find_first_bad_number(message, buffer_size):
    buffer = CircularBuffer(message[:buffer_size])
    for i in range(buffer_size, len(message)):
        current_number = message[i]
        valid = False
        for j in range(buffer_size - 1):
            for k in range(j + 1, buffer_size):
                if buffer[j] + buffer[k] == current_number:
                    valid = True
                    break
            if valid:
                break
        if valid:
            buffer.append(current_number)
        else:
            return current_number


def get_summing_set(message, num):
    start = 0
    end = 1
    message_slice = message[start:end+1]
    slice_sum = sum(message_slice)
    while slice_sum != num or start == end:
        if slice_sum < num or start == end:  # The sum must consist of at least two numbers
            end += 1
        elif slice_sum > num:
            start += 1

        if end == len(message):  # end has exceeded the length of the array; the message is invalid
            return None

        message_slice = message[start:end + 1]
        slice_sum = sum(message_slice)
    return min(message_slice) + max(message_slice)


if __name__ == '__main__':
    data = parse_input('input.txt')
    first_bad_num = find_first_bad_number(data, 25)
    print('First bad number: {}'.format(first_bad_num))
    weakness = get_summing_set(data, first_bad_num)
    print('Encryption weakness: {}'.format(weakness))
