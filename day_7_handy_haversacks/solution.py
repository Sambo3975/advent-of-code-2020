import regex as re  # This supports repeating capture groups, unlike the built-in 're'
pattern = re.compile(r'^(\w+ \w+) bags contain(?:,? (\d*) ?(\w+ \w+) bags?)+.$')


def parse_bag_rules(file_name):
    bag_rules = {}
    with open(file_name) as f:
        for line in f.readlines():
            match = re.fullmatch(pattern, line[:-1])
            if match is not None:
                container_color = match.group(1)

                contents = []
                quantities = match.captures(2)
                colors = match.captures(3)
                for quantity, color in zip(quantities, colors):
                    # The quantity string will be empty if the rule is 'x bags contain no other bags'
                    if len(quantity) > 0:
                        contents.append((color, int(quantity)))

                bag_rules[container_color] = contents

    return bag_rules


def can_contain_gold(bag_rules, bag_color, checked_bag_colors):
    if bag_color in checked_bag_colors:
        return checked_bag_colors[bag_color]  # Whether this bag can contain a gold bag has already been determined

    color_rules = bag_rules[bag_color]
    if len(color_rules) == 0:
        checked_bag_colors[bag_color] = False
        return False  # This bag must contain no others
    else:
        for contents in color_rules:
            if contents[0] == 'shiny gold':
                checked_bag_colors[bag_color] = True
                return True  # This bag must directly contain a gold bag
            else:
                # This bag may contain a bag that must directly contain a gold bag
                can_contain = can_contain_gold(bag_rules, contents[0], checked_bag_colors)
                checked_bag_colors[bag_color] = can_contain
                if can_contain:
                    return True


def count_bags_containing_gold(bag_rules):
    checked_bag_colors = {}
    gold_containing_bags = 0
    for key in bag_rules:
        if can_contain_gold(bag_rules, key, checked_bag_colors):
            gold_containing_bags += 1
    return gold_containing_bags


def count_bags_inside(bag_rules, bag_color):
    bag_count = 0
    color_rules = bag_rules[bag_color]
    for rule in color_rules:
        bag_count += rule[1]
        bag_count += count_bags_inside(bag_rules, rule[0]) * rule[1]
    return bag_count


if __name__ == '__main__':
    rules = parse_bag_rules('input.txt')
    count = count_bags_containing_gold(rules)
    print('Number of bags that can (eventually) contain a shiny gold bag: {}'.format(count))
    count = count_bags_inside(rules, 'shiny gold')
    print('Number of bags a shiny gold bag must contain: {}. Good luck with that!'.format(count))
