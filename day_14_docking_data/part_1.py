from bitarray import bitarray
from bitarray.util import ba2int, int2ba
import re
instruction_pattern = re.compile(r"^mem\[(\d+)] = (\d+)$")


class DecoderChipV1:

    @staticmethod
    def str_to_bool(string):
        return False if string == '0' else True

    @staticmethod
    def str_to_bitarray(string):
        return bitarray(string.zfill(36))

    @staticmethod
    def parse_mask(mask):
        new_mask = {}
        mask_raw = mask[-37:-1]
        for i in range(len(mask_raw)):
            if mask_raw[i] in ['0', '1']:
                new_mask[i] = DecoderChipV1.str_to_bool(mask_raw[i])
        return new_mask

    def __init__(self):
        self.__mask = None
        self.__mem = None
        self.__instructions = None
        self.__iter = None

    def __getitem__(self, item):
        if item < 0 or item > 0xfffffffff:
            raise IndexError("Index out of range. Index must be representable as a 36-bit unsigned integer.")
        if item in self.__mem:
            return self.__mem[item]
        return DecoderChipV1.str_to_bitarray('0')

    def __setitem__(self, key, value):
        if key < 0 or key > 0xfffffffff:
            raise IndexError("Index out of range. Index must be representable as a 36-bit unsigned integer.")
        value_as_int = int(value)
        if value_as_int < 0 or value_as_int > 0xfffffffff:
            raise ValueError("Invalid value. Value must be representable as a 36-bit unsigned integer.")

        value = int2ba(value, length=36)
        if self.__mask is not None:
            for item in self.__mask:
                value[item] = self.__mask[item]

        self.__mem[key] = value

    def __repr__(self):
        keys = [key for key in self.__mem]
        width = len(str(max(keys)))

        string = 'BitmaskComputer'
        for k in sorted(keys):
            string += f"\n  {str(k).rjust(width)}: {self[k]} ({ba2int(self[k])})"
        return string

    def load(self, file_name):
        with open(file_name) as f:
            lines = f.readlines()

        self.__mask = None

        self.__mem = {}

        # Parse the instructions
        self.__instructions = []
        for line in lines:
            match = re.match(instruction_pattern, line)
            if match is not None:
                self.__instructions.append((int(match.group(1)), int(match.group(2))))
            else:
                self.__instructions.append(self.parse_mask(line))

    def execute(self):
        for instruction in self.__instructions:
            if len(instruction) == 2:
                self[instruction[0]] = instruction[1]
            else:
                self.__mask = instruction

    def all_mem(self):
        """Get a dictionary of all non-zero entries in memory"""
        return self.__mem


if __name__ == '__main__':
    computer = DecoderChipV1()
    computer.load('input.txt')
    computer.execute()
    memory = computer.all_mem()
    mem_sum = 0
    for k in memory:
        mem_sum += ba2int(memory[k])
    print(f"Sum of memory: {mem_sum}")
