from bitarray import bitarray
from bitarray.util import ba2int, int2ba
import re
instruction_pattern = re.compile(r"^mem\[(\d+)] = (\d+)$")


class DecoderChipV2:

    @staticmethod
    def str_to_bool(string):
        return False if string == '0' else True

    @staticmethod
    def str_to_bitarray(string):
        return bitarray(string.zfill(36))

    @staticmethod
    def parse_mask(mask):
        new_mask = ''
        floating = []
        mask_raw = mask[-37:-1]
        for i in range(len(mask_raw)):
            if mask_raw[i] == 'X':
                floating.append(i)
                new_mask += '0'
            else:
                new_mask += mask_raw[i]
        return bitarray(new_mask), floating

    @staticmethod
    def get_write_addresses(address, mask, floating):
        address = address.copy() | mask
        address_list = []
        max_floating = 2 ** len(floating)
        for i in range(max_floating):
            float_bits = int2ba(i, length=len(floating))
            new_address = address.copy()
            for j in range(len(float_bits)):
                new_address[floating[j]] = float_bits[j]
            address_list.append(new_address)
        return [ba2int(a) for a in address_list]

    def __init__(self):
        self.__mask = None
        self.__floating = None
        self.__mem = None
        self.__instructions = None
        self.__iter = None

    def __getitem__(self, item):
        if item < 0 or item > 0xfffffffff:
            raise IndexError("Index out of range. Index must be representable as a 36-bit unsigned integer.")
        if item in self.__mem:
            return self.__mem[item]
        return DecoderChipV2.str_to_bitarray('0')

    def __setitem__(self, key, value):
        if key < 0 or key > 0xfffffffff:
            raise IndexError("Index out of range. Index must be representable as a 36-bit unsigned integer.")
        value_as_int = int(value)
        if value_as_int < 0 or value_as_int > 0xfffffffff:
            raise ValueError("Invalid value. Value must be representable as a 36-bit unsigned integer.")

        key = int2ba(key, length=36)
        value = int2ba(value, length=36)

        if self.__mask is not None:
            write_addresses = self.get_write_addresses(key, self.__mask, self.__floating)
            for address in write_addresses:
                self.__mem[address] = value
        else:
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
            if isinstance(instruction[0], int):
                self[instruction[0]] = instruction[1]
            else:
                self.__mask, self.__floating = instruction

    def all_mem(self):
        """Get a dictionary of all non-zero entries in memory"""
        return self.__mem


if __name__ == '__main__':
    computer = DecoderChipV2()
    computer.load('input.txt')
    computer.execute()
    memory = computer.all_mem()
    mem_sum = 0
    for a in memory:
        mem_sum += ba2int(memory[a])
    print(f"Sum of memory: {mem_sum}")
