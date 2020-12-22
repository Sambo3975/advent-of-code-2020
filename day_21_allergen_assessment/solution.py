import regex as re
ingredient_list_pattern = re.compile(r"^(?:(\w+) )+\(contains(?:,? (\w+))+\)$")


class Set:
    """A (strictly finite) mathematical set"""

    def __init__(self, data=None):
        self.__data = {}
        if data is not None:
            for x in data:
                self.insert(x)

    def __contains__(self, item):
        return item in self.__data

    def __repr__(self):
        return "Set(" + ', '.join(self.contents()) + ")"

    def __len__(self):
        return len(self.__data)

    def insert(self, item):
        self.__data[item] = True  # Inserting the same element multiple times has no effect

    def remove(self, item):
        self.__data.pop(item, None)  # Removing an element that is not contained has no effect

    def contents(self):
        return [k for k in self.__data]

    def union(self, other):
        new = Set(self.contents())
        [new.insert(x) for x in other.contents()]
        return new

    def intersection(self, other):
        new = Set()
        for item in self.contents():
            if item in other:
                new.insert(item)
        return new


def open_file(file_name):
    lists = []
    all_ingredients = []  # List of all ingredients. Contains repeats.
    with open(file_name) as f:
        data = f.readlines()
    for x in data:
        match = re.match(ingredient_list_pattern, x)
        lists.append((match.captures(1), match.captures(2)))
        all_ingredients.extend(match.captures(1))
    return lists, all_ingredients


def deduce_ingredients_containing_no_allergens(data):
    ingredients_not_containing_allergen = Set()
    allergen_to_possible_ingredients = {}  # allergen: Set of ingredient

    for x in data:
        for allergen in x[1]:
            [ingredients_not_containing_allergen.insert(ingredient) for ingredient in x[0]]
            if allergen not in allergen_to_possible_ingredients:
                # Get a starting point for which ingredients may contain the allergen.
                allergen_to_possible_ingredients[allergen] = Set([ingredient for ingredient in x[0]])
            else:
                # Ingredient must be in both foods with the allergen, or it cannot contain that allergen.
                allergen_to_possible_ingredients[allergen] =\
                    allergen_to_possible_ingredients[allergen].intersection(Set([ingredient for ingredient in x[0]]))

    for ingredient in ingredients_not_containing_allergen.contents():
        for allergen in allergen_to_possible_ingredients:
            if ingredient in allergen_to_possible_ingredients[allergen]:
                ingredients_not_containing_allergen.remove(ingredient)

    return ingredients_not_containing_allergen, allergen_to_possible_ingredients


def count_hypoallergenic_ingredients(hypoallergenic_ingredients, all_ingredients):
    count = 0
    for ingredient in all_ingredients:
        if ingredient in hypoallergenic_ingredients:
            count += 1
    return count


def list_dangerous_ingredients(allergen_to_possible_ingredients):
    non_located_allergen_count = len(allergen_to_possible_ingredients)
    allergen_to_ingredient = {}

    while non_located_allergen_count > 0:
        rm_keys = []
        for key in allergen_to_possible_ingredients:
            if len(allergen_to_possible_ingredients[key]) == 1:
                allergen_to_ingredient[key] = allergen_to_possible_ingredients[key].contents()[0]
                rm_keys.append(key)
                non_located_allergen_count -= 1
                ingredient = allergen_to_ingredient[key]
                for s in allergen_to_possible_ingredients.values():
                    s.remove(ingredient)
        if len(rm_keys) == 0:
            raise ValueError("Not enough data to generate list.")
        for key in rm_keys:
            allergen_to_possible_ingredients.pop(key)

    return ','.join([allergen_to_ingredient[k] for k in sorted(allergen_to_ingredient.keys())])


if __name__ == '__main__':
    ingredient_lists, ingredients_of_all_foods = open_file('input.txt')
    safe_ingredients, allergens = deduce_ingredients_containing_no_allergens(ingredient_lists)
    hypoallergenic_count = count_hypoallergenic_ingredients(safe_ingredients, ingredients_of_all_foods)
    print(f"Total appearances of safe ingredients: {hypoallergenic_count}")
    unsafe_ingredients = list_dangerous_ingredients(allergens)
    print(f"Dangerous ingredients: {unsafe_ingredients}")
