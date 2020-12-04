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


required_fields = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid'
]


def check_bounded(value, mini, maxi):
    return mini <= int(value) <= maxi


def check_height(value):
    number = value[:-2]
    unit = value[-2:]
    return unit == 'cm' and check_bounded(number, 150, 193) \
        or unit == 'in' and check_bounded(number, 59, 76)


def check_hair_color(value):
    return re.match(r'^#([0-9]|[a-f]){6}$', value)


valid_eye_colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def check_eye_color(value):
    return value in valid_eye_colors


def check_passport_id(value):
    return re.match(r'^[0-9]{9}$', value)


def validate_passports(passports):
    valid_ct = 0
    for passport in passports:
        invalid = False
        # Check for each required field
        for field in required_fields:
            if field not in passport:
                invalid = True
        if not invalid:
            valid_ct += 1
    return valid_ct


def validate_passports_properly(passports):
    valid_ct = 0
    for x in passports:
        print(x)
        invalid = False
        # Check for each required field
        for field in required_fields:
            if field not in x:
                invalid = True
                break
        print('passed first check')

        # Check fields for valid values
        if not invalid \
                and check_bounded(x['byr'], 1920, 2002) \
                and check_bounded(x['iyr'], 2010, 2020) \
                and check_bounded(x['eyr'], 2020, 2030) \
                and check_height(x['hgt']) \
                and check_hair_color(x['hcl']) \
                and check_eye_color(x['ecl']) \
                and check_passport_id(x['pid']):
            print('passed second check')
            valid_ct += 1

    return valid_ct


if __name__ == '__main__':
    passes = read_input('input.txt')

    # Part 1
    valid_ct = validate_passports(passes)
    print('Valid passports: {}'.format(valid_ct))

    # Part 2
    valid_ct = validate_passports_properly(passes)
    print('Validly Valid passports: {}'.format(valid_ct))
