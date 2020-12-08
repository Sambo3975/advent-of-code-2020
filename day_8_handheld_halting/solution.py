import re
instruction_pattern = re.compile(r'^(\w{3}) \+?(-?\d+)$')


# This year, I'm keeping each iteration of the computer locally so I can see how it evolved later.
# I mean, I assume there will be multiple iterations like with the Intcode computer from last year.
class SpaghettiComputer:
    """For lack of a better name. A simple spaghetti code processor."""

    def __init__(self):
        self.__ops = {
            'nop': self.nop,
            'jmp': self.jmp,
            'acc': self.acc
        }
        self.__memory = None
        self.__address = 0
        self.__accumulator = 0
        self.__current_file = ''

    # File loading and parsing

    def parse(self, file_name):
        self.__current_file = file_name
        self.__memory = []
        with open(file_name) as f:
            for line in f.readlines():
                match = re.match(instruction_pattern, line)
                self.__memory.append([match.group(1), int(match.group(2))])

    # Execution

    def execute(self, file_name):
        if self.__current_file != file_name:
            self.parse(file_name)

        self.__address = 0
        self.__accumulator = 0
        debug_list = [False for _ in range(len(self.__memory))]
        while not debug_list[self.__address]:
            debug_list[self.__address] = True
            current_instruction = self.__memory[self.__address]
            op = current_instruction[0]
            arg = current_instruction[1]
            self.__ops[op](arg)
            if self.__address == len(self.__memory):
                return True, self.__accumulator  # Finished execution
        return False, self.__accumulator  # Stuck in a loop

    def fix_corrupted_instruction(self, file_name):
        self.parse(file_name)

        # Locate all 'nop' and 'jmp' instructions
        nops = []
        jmps = []
        mem = self.__memory
        for i in range(len(mem)):
            if mem[i][0] == 'nop':
                nops.append(i)
            if mem[i][0] == 'jmp':
                jmps.append(i)

        # Try to fix the broken instruction using simple brute force. I couldn't think of a better way.
        for ops in [nops, jmps]:
            for i in ops:
                mem[i][0] = 'jmp' if mem[i][0] == 'nop' else 'nop'
                success, accumulator = self.execute(file_name)
                if success:
                    return accumulator
                mem[i][0] = 'jmp' if mem[i][0] == 'nop' else 'nop'

    # Operations

    def nop(self, arg):
        """nop: does nothing; arg is ignored"""
        self.__address += 1

    def acc(self, arg):
        """acc: add arg to accumulator"""
        self.__accumulator += arg
        self.__address += 1

    def jmp(self, arg):
        """jmp: relative jump to address"""
        self.__address += arg


if __name__ == '__main__':
    computer = SpaghettiComputer()
    _, accumulator_value = computer.execute('input.txt')
    print('Accumulator at {} on first repeated instruction.'.format(accumulator_value))
    accumulator_value = computer.fix_corrupted_instruction('input.txt')
    print('Successfully fixed loop with accumulator value {}.'.format(accumulator_value))
