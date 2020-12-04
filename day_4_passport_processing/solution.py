import re


def read_input(file_name):
    passports = []
    with open(file_name) as f:
        contents = f.read().split('\n\n')
        for x in contents:
            data = {}
            for substring in x.split():
                splits = substring.split(':')
                data[splits[0]] = splits[1].strip()
            passports.append(data)
    return passports


def check_height(value):
    number = int(value[:-2])
    unit = value[-2:]
    return unit == 'cm' and 150 <= number <= 193 \
        or unit == 'in' and 59 <= number <= 76


valid_eye_colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
field_checks = {
    'byr': lambda value: 1920 <= int(value) <= 2002,
    'iyr': lambda value: 2010 <= int(value) <= 2020,
    'eyr': lambda value: 2020 <= int(value) <= 2030,
    'hgt': check_height,
    'hcl': lambda value: re.match(r'^#([0-9]|[a-f]){6}$', value),
    'ecl': lambda value: value in valid_eye_colors,
    'pid': lambda value: re.match(r'^[0-9]{9}$', value)
}


def validate_passports(passports, check_fields=True):
    valid_count = 0
    for x in passports:
        invalid = False
        # Check for each required field
        for field in field_checks:
            if not (field in x and (not check_fields or field_checks[field](x[field]))):
                invalid = True
                break
        if not invalid:
            valid_count += 1
    return valid_count


if __name__ == '__main__':
    passes = read_input('input.txt')

    # Part 1
    valid_ct = validate_passports(passes, False)
    print('Passports with all required fields: {}'.format(valid_ct))

    # Part 2
    valid_ct = validate_passports(passes)
    print('Valid passports: {}'.format(valid_ct))
