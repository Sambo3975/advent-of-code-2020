from numpy import array
motion_vector_map = {
    # Cardinal direction to motion vector
    'E': array([1, 0]),
    'N': array([0, -1]),
    'W': array([-1, 0]),
    'S': array([0, 1]),
    # Numeric bearing to motion vector; standard position
    0: array([1, 0]),
    90: array([0, -1]),
    180: array([-1, 0]),
    270: array([0, 1]),
}
orthogonal_rotations = {
    270: lambda p: array([-p[1], p[0]]),
    180: lambda p: -p,
    90: lambda p: array([p[1], -p[0]]),
}


def parse_file(file_name):
    with open(file_name) as f:
        return [[x[0], int(x[1:])] for x in f.readlines()]


def manhattan_distance_from_origin(p):
    return abs(p[0]) + abs(p[1])


def get_destination(directions):
    ferry_position = array([0, 0])
    ferry_bearing = 0
    for d in directions:
        if d[0] == 'F':
            ferry_position += motion_vector_map[ferry_bearing] * d[1]
        elif d[0] in ['L', 'R']:
            ferry_bearing = (ferry_bearing + (1 if d[0] == 'L' else -1) * d[1]) % 360
        else:
            ferry_position += motion_vector_map[d[0]] * d[1]
    return ferry_position


def get_destination_properly(directions):
    ferry_position = array([0, 0])
    waypoint_position = array([10, -1])
    for d in directions:
        if d[0] == 'F':
            ferry_position += waypoint_position * d[1]
        elif d[0] in ['L', 'R']:
            waypoint_position = orthogonal_rotations[((1 if d[0] == 'L' else -1) * d[1]) % 360](waypoint_position)
        else:
            waypoint_position += motion_vector_map[d[0]] * d[1]
    return ferry_position


def repr_position(pos):
    return f"{'W' if pos[0] < 0 else 'E'} {abs(pos[0])}, {'S' if pos[1] > 0 else 'N'} {abs(pos[1])}"


if __name__ == '__main__':
    direction_list = parse_file('input.txt')
    for wrong in [True, False]:
        print(f"When done {'wrong' if wrong else 'right'}:")
        destination_func = get_destination if wrong else get_destination_properly
        destination = destination_func(direction_list)
        distance = manhattan_distance_from_origin(destination)
        print(f"  Final position: {repr_position(destination)}; Manhattan distance from origin: {distance}.")
