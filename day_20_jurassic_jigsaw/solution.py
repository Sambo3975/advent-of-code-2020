from colr import Colr

border_to_opposite = {
    'top': 'bottom',
    'bottom': 'top',
    'left': 'right',
    'right': 'left',
}


class PuzzlePiece:

    def __init__(self, data):
        data = data.split('\n')
        self.id = int(data[0][5:9])
        self.data = []
        for row in data[1:]:
            self.data.append([x for x in row])
        self.borders = self.__get_borders()

    def __repr__(self):
        string = f"Tile {self.id}:\n"
        for row in self.data:
            string += ''.join(row)
            string += '\n'
        return string

    def __get_borders(self):
        return {
            'top': list(self.data[0]),
            'right': [x[-1] for x in self.data],
            'left': [x[0] for x in self.data],
            'bottom': list(self.data[-1]),
        }

    def get_matches_with_piece(self, other):
        matches = []
        borders = self.borders
        flipped = False
        # print(f"\nComparing tile {self.id} with tile {other.id}")
        for i in range(2):
            for j in range(4):
                other_borders = other.borders
                # print(f"Comparing border sets. Rotation: {j}; Flipped: {flipped}")
                for key in borders:
                    # print(f"  {key:6} {borders[key]} <=> {border_to_opposite[key]:6} "
                    #       f"{other_borders[border_to_opposite[key]]}", end='')
                    if borders[key] == other_borders[border_to_opposite[key]]:
                        # print(Colr().green(" MATCH -> "), end='')
                        matches.append((key, j, flipped))
                        # print(matches[-1], end='')
                    # print('')
                other.rotate(1)
            other.flip()
            flipped = True
        return matches

    def get_matches_with_pieces(self, others, skip=None):
        all_matches = []
        for i in range(len(others)):
            if skip is not None and i == skip:
                continue
            o = others[i]
            matches = self.get_matches_with_piece(o)
            # print(f"sid: {self.id}; oid: {o.id}")
            if len(matches) > 0:
                for m in matches:
                    all_matches.append((o.id, m[0], m[1], m[2]))
        return all_matches
    
    def rotate(self, clockwise_turns):
        if clockwise_turns == 0:
            self.data = self.data
        elif clockwise_turns in [1, 2]:  # CW 90 degrees
            self.data = list(zip(*self.data[::-1]))
        if clockwise_turns == 2:  # 180 degrees
            self.data = list(zip(*self.data[::-1]))
        elif clockwise_turns == 3:  # CCW 90 degrees
            self.data = list(zip(*self.data))[::-1]
        self.borders = self.__get_borders()

    def flip(self):
        self.data = [row[::-1] for row in self.data]
        self.borders = self.__get_borders()


def parse_file(file_name):
    with open(file_name) as f:
        return [PuzzlePiece(x) for x in f.read()[:-1].split('\n\n')]


if __name__ == '__main__':
    pieces = parse_file('test.txt')
    for i in range(len(pieces) - 1):
        print(f"{pieces[i].id}: {pieces[i].get_matches_with_pieces(pieces, skip=i)}")
