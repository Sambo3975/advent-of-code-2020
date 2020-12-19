from copy import copy, deepcopy


class MagicGrid:
    """An "infinite" n-dimensional grid"""

    def __init__(self, other=None, dimensionality=2, fill=' '):
        """
        Constructor
        :param other: The MagicGrid to copy. If this is set, all other parameters will be ignored.
        :param dimensionality: The dimensionality of the grid (default = 2, minimum = 1).
        :type dimensionality: int
        :param fill: The value to return when indexing a position with no value defined.
        """
        if other is not None:
            self.__data = other.__data.copy()
            self.__dimensionality = other.__dimensionality
            self.__extents = deepcopy(other.__extents)
            self.fill = other.fill
        else:
            self.__data = {}
            self.__dimensionality = dimensionality
            # List of lists [a, b], where a is the lowest extent in that dimension and b is the highest
            self.__extents = [[0, 0] for _ in range(dimensionality)]
            self.fill = fill
            
    def __repr__(self):
        dim = self.__dimensionality
        if dim > 4:
            raise NotImplementedError(f"String representation of {dim}-dimensional MagicGrid not implemented.")

        ranges = []
        for i in range(4):
            if 4 - i <= dim:
                print(i)
                ranges.append(self.get_dimensional_range(3 - i))
            else:
                ranges.append(range(1))

        print(ranges)

        string = ''
        for w in ranges[0]:
            for z in ranges[1]:
                if dim >= 3:
                    string += f"\nz={z}"
                if dim == 4:
                    string += f", w={w}"
                for y in ranges[2]:
                    if dim >= 2:
                        string += '\n'
                    for x in ranges[3]:
                        if (w, z, y, x) in self:
                            string += self[w, z, y, x]
                        elif (z, y, x) in self:
                            string += self[z, y, x]
                        elif (y, x) in self:
                            string += self[y, x]
                        elif x in self:
                            return self[x]
                        else:
                            string += self.fill
                if dim >= 3:
                    string += '\n'

        return string

    def __getitem__(self, item):
        self.__validate_index(item)
        if item in self:
            return self.__data[item]
        return self.fill

    def __setitem__(self, key, value):
        self.__validate_index(key)
        if value is not None:
            self.__update_extents(key)
            self.__data[key] = value
        else:
            self.__data.pop(key, None)

    def __len__(self):
        return len(self.__data)

    def __copy__(self):
        return MagicGrid(self)

    def __contains__(self, item):
        return item in self.__data

    def __validate_index(self, index):
        if self.__dimensionality == 1:
            if not isinstance(index, int):
                raise IndexError("Invalid index structure or type. Must be an int.")
            return
        if not (isinstance(index, tuple) or isinstance(index, list)) or len(index) != self.__dimensionality:
            raise IndexError(f"Invalid index structure. Must be a tuple or list of length {self.__dimensionality}")
        else:
            for v in index:
                if not isinstance(v, int):
                    raise IndexError(f"{v}: Invalid coordinate type: '{type(v)}'")
                
    def __update_extents(self, key):
        ext = self.__extents
        if self.__dimensionality == 1:
            ext[0][0] = min(key, ext[0][0])
            ext[0][0] = min(key, ext[0][1])
        else:
            for i in range(self.__dimensionality):
                ext[i][0] = min(key[i], ext[i][0])
                ext[i][1] = max(key[i], ext[i][1])

    def get_dimensional_length(self, dim):
        if isinstance(dim, int) and 0 <= dim < self.__dimensionality:
            ext = self.__extents
            return ext[dim][1] - ext[dim][0] + 1
        else:
            raise IndexError("Invalid dimensional index.")

    def get_dimensional_range(self, dim, margin=0):
        if isinstance(dim, int) and 0 <= dim < self.__dimensionality:
            ext = self.__extents
            return range(ext[dim][0] - margin, ext[dim][1] + margin + 1)
        else:
            raise IndexError("Invalid dimensional index.")

    def get_dimensionality(self):
        return self.__dimensionality


def parse_file(file_name, dim=3):
    with open(file_name) as f:
        lines = f.read().split()
    data = MagicGrid(dimensionality=dim, fill='.')
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] == '#':
                if dim == 3:
                    data[0, y, x] = '#'
                else:
                    data[0, 0, y, x] = '#'
    return data


def get_next_state_cube(z, y, x, current_state, w=None):
    alive = (z, y, x) in current_state

    # If the cube is alive, it shouldn't be counted as its own living neighbor
    living_adjacent_count = -1 if alive else 0

    if w is not None:
        w_range = range(w-1, w+2)
    else:
        w_range = range(1)

    for cw in w_range:
        for cz in range(z-1, z+2):
            for cy in range(y-1, y+2):
                for cx in range(x-1, x+2):
                    if (w is None and (cz, cy, cx) in current_state) or (cw, cz, cy, cx) in current_state:
                        living_adjacent_count += 1
                    if w == 0 and z == 0 and y == 0 and x == 0 and cz == 0 and cw == 0:
                        print(cx, cy, cz, cw)
                        print(current_state[cw, cz, cy, cx])

    if alive and living_adjacent_count < 2 or living_adjacent_count > 3:
        return False
    elif not alive and living_adjacent_count == 3:
        return True
    return alive


def get_next_state_grid(current_state, in_4d=False):
    next_state = copy(current_state)
    if in_4d:
        w_range = current_state.get_dimensional_range(0, 1)
        off = 1
    else:
        w_range = range(1)
        off = 0
    for w in w_range:
        for z in current_state.get_dimensional_range(off, 1):
            for y in current_state.get_dimensional_range(off+1, 1):
                for x in current_state.get_dimensional_range(off+2, 1):
                    if not in_4d:
                        if get_next_state_cube(z, y, x, current_state):
                            next_state[z, y, x] = '#'
                        else:
                            next_state[z, y, x] = None
                    else:
                        if get_next_state_cube(z, y, x, current_state, w):
                            next_state[w, z, y, x] = '#'
                        else:
                            next_state[w, z, y, x] = None
    return next_state


def iterate_grid(grid, steps, verbose=False):
    in_4d = grid.get_dimensionality() == 4
    if verbose:
        print("Before any cycles:")
        print(grid)
    for i in range(steps):
        grid = get_next_state_grid(grid, in_4d)
        if verbose:
            print(f"After {i + 1} cycle{'' if i == 0 else 's'}:")
            print(grid)
    return grid


if __name__ == '__main__':
    # conway_grid = parse_file('test.txt', 3)
    # conway_grid = iterate_grid(conway_grid, 1, verbose=True)
    # print(f"Final active count: {len(conway_grid)}")
    grid1 = MagicGrid(dimensionality=1, fill='.')
    grid1[-1] = '#'
    grid1[2] = '#'
    print(grid1)

