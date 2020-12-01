class Utils:
    """Some utility functions for Advent of Code 2020"""

    @staticmethod
    def read_ints(file_name):
        """Read a file, line by line, as a list of integers"""
        ints = []
        with open(file_name) as f:
            for line in f.readlines():
                ints.append(int(line))
        return ints

