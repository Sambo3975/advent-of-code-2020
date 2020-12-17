import re
from collections import deque


field_rule_pattern = re.compile(r"^([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)$")


class Interval:
    """A simple inclusive interval class for integers"""

    def __init__(self, lo, hi):
        self.lo = lo
        self.hi = hi

    def __contains__(self, item):
        return self.lo <= item <= self.hi

    def __repr__(self):
        return f"[{self.lo}, {self.hi}]"

    def range(self):
        return self.hi - self.lo + 1


def parse_field_rules(rules_raw):
    ticket_rules = {}
    for x in rules_raw.split('\n'):
        groups = re.match(field_rule_pattern, x).groups()
        ticket_rules[groups[0]] = (Interval(int(groups[1]), int(groups[2])), Interval(int(groups[3]), int(groups[4])))
    return ticket_rules


def parse_ticket(ticket_raw):
    return [int(x) for x in ticket_raw.split(',')]


def parse_tickets(nearby_tickets_raw):
    tickets = [parse_ticket(x) for x in nearby_tickets_raw.split('\n')[1:-1]]
    return tickets


def parse_file(file_name):
    r"""
    Parse the ticket data file. It should be formatted like the following example:

    class: 1-3 or 5-7
    row: 6-11 or 33-44
    seat: 13-40 or 45-50

    your ticket:
    7,1,14

    nearby tickets:
    7,3,47
    40,4,50
    55,2,20
    38,6,12

    :param file_name:
    :return: rules, my_ticket, nearby_tickets
    """
    with open(file_name) as f:
        data = f.read().split('\n\n')
    return parse_field_rules(data[0]), parse_ticket(data[1].split('\n')[1]), parse_tickets(data[2])


def get_invalid_field_values_single_ticket(ticket, field_rules, invalid_field_values):
    for field in ticket:
        valid = False
        for rule in field_rules.values():
            if field in rule[0] or field in rule[1]:
                valid = True
                break
        if not valid:
            invalid_field_values.append(field)


def get_invalid_field_values_all_tickets(tickets, field_rules):
    invalid_field_values = []
    valid_tickets = []
    for t in tickets:
        pre_check_len = len(invalid_field_values)
        get_invalid_field_values_single_ticket(t, field_rules, invalid_field_values)
        if len(invalid_field_values) == pre_check_len:  # No invalid values were added; ticket is valid
            valid_tickets.append(t)
    return invalid_field_values, valid_tickets


def check_ticket_rule(ticket_rules, rule_name, value):
    ticket_rule = ticket_rules[rule_name]
    return value in ticket_rule[0] or value in ticket_rule[1]


def deduce_position_of_field(field_rules, taken_numbers, key, valid_tickets, indices):
    for t in valid_tickets:
        i_max = len(indices)
        i = 0
        while i < i_max and len(indices) > 1:
            idx = indices.popleft()
            if idx not in taken_numbers and check_ticket_rule(field_rules, key, t[idx]):
                # Skip positions that have been taken
                indices.append(idx)
            i += 1
        if len(indices) == 1:
            break
    return indices


def deduce_position_of_all_fields(valid_tickets, field_rules):
    all_indices = deque(range(len(field_rules.keys())))
    positions = {}
    # The fields with the tightest intervals of valid values will eliminate the most possibilities
    sorted_keys = sorted(field_rules.keys(), key=lambda x: field_rules[x][0].range() + field_rules[x][1].range())
    # Allows us to immediately eliminate positions that are taken
    taken_positions = {}
    # Used as a check to see if all keys' positions have been narrowed down to a single possibility
    total_available_positions = len(valid_tickets[0])
    # Allows us to skip keys whose positions have already been determined
    taken_keys = {}

    while len(taken_positions) < total_available_positions:
        for key in sorted_keys:
            if key in taken_keys:
                continue  # Key's position is already known
            if key not in positions:
                positions[key] = all_indices.copy()
            positions[key] = deduce_position_of_field(field_rules, taken_positions, key, valid_tickets, positions[key])
            if len(positions[key]) == 1:
                taken_positions[positions[key][0]] = True
                taken_keys[key] = True

    for key in positions:
        positions[key] = positions[key][0]
    return positions


if __name__ == '__main__':
    rules, my_ticket, nearby_tickets = parse_file('input.txt')
    invalid_values, good_tickets = get_invalid_field_values_all_tickets(nearby_tickets, rules)
    assert len(good_tickets) + len(invalid_values) == len(nearby_tickets), "Wrong number of tickets removed!"
    print(f"Ticket scanning error rate: {sum(invalid_values)}")

    field_positions = deduce_position_of_all_fields(good_tickets, rules)
    prod = 1
    for k in field_positions:
        if k[:9] == 'departure':
            prod *= my_ticket[field_positions[k]]
    print(f"Product of departure fields: {prod}")
