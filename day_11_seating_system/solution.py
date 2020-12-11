from copy import deepcopy


# Class code created by Stack Overflow user NichtJens
class CharList(list):

    def __init__(self, s):
        list.__init__(self, s)

    @property
    def list(self):
        return list(self)

    @property
    def string(self):
        return "".join(self)

    def __setitem__(self, key, value):
        if isinstance(key, int) and len(value) != 1:
            cls = type(self).__name__
            raise ValueError("attempt to assign sequence of size {} to {} item of size 1".format(len(value), cls))
        super(CharList, self).__setitem__(key, value)

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string


def read_file(file_name):
    with open(file_name) as f:
        return [CharList(x[:-1]) for x in f.readlines()]


offsets = []


def construct_offsets():
    global offsets
    for y in range(-1, 2):
        for x in range(-1, 2):
            if x != 0 or y != 0:
                offsets.append((y, x))


def next_seat_state(seats, y, x):
    width = len(seats[0])
    height = len(seats)

    adjacent_count = 0
    for o in offsets:
        cx = x + o[0]
        cy = y + o[1]
        if 0 <= cy < height and 0 <= cx < width and seats[cy][cx] == '#':
            adjacent_count += 1

    if seats[y][x] == 'L' and adjacent_count == 0:
        return '#'
    if seats[y][x] == '#' and adjacent_count >= 4:
        return 'L'
    return seats[y][x]


def next_seat_state_line_of_sight(seats, y, x):
    width = len(seats[0])
    height = len(seats)

    visible_count = 0
    for o in offsets:
        dx = o[0]
        dy = o[1]
        cx = x
        cy = y
        while True:
            cx += dx
            cy += dy
            if cx < 0 or cx >= width or cy < 0 or cy >= height or seats[cy][cx] == 'L':
                break  # saw the wall or an empty seat
            elif seats[cy][cx] == '#':
                visible_count += 1  # saw an occupied seat
                break
            # Saw nothing; look out farther

    if seats[y][x] == 'L' and visible_count == 0:
        return '#'
    if seats[y][x] == '#' and visible_count >= 5:
        return 'L'
    return seats[y][x]


def get_next_state(seats, line_of_sight=False):
    new_seats = deepcopy(seats)
    update_function = next_seat_state_line_of_sight if line_of_sight else next_seat_state

    for y in range(len(seats)):
        for x in range(len(seats[0])):
            if seats[y][x] != '.':  # Make sure there's a seat at this position
                new_seats[y][x] = update_function(seats, y, x)

    return new_seats


def seats_have_changed(old, new):
    for y in range(len(old)):
        for x in range(len(old[0])):
            if old[y][x] != new[y][x]:
                return True
    return False


def count_occupied(seats):
    count = 0
    for y in range(len(seats)):
        for x in range(len(seats[0])):
            if seats[y][x] == '#':
                count += 1
    return count


def print_seats(seats):
    for row in seats:
        print(row)
    print('')


if __name__ == '__main__':
    construct_offsets()

    for look_far in [False, True]:
        seat_list = read_file('input.txt')
        while True:
            next_state = get_next_state(seat_list, look_far)
            if not seats_have_changed(seat_list, next_state):
                break
            seat_list = next_state
        occupied = count_occupied(seat_list)
        print(f"Seat occupancy has stabilized at {occupied} when {'' if look_far else 'not '}looking far.")
