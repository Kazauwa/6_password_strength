import sys
import re


def load_blacklist(path):
    with open(path, 'r') as reader:
        blacklist = reader.read()
    blacklist = re.split('\s+', blacklist)
    return blacklist


def has_mixed_case(password):
    if not password.isupper() and not password.islower():
        return True
    print('\nPassword does not consist of mixed case!')
    return False


def has_digit(password):
    if re.findall('\d+', password):
        return True
    print('\nPassword does not contain any digits!')
    return False


def has_special_chars(password):
    if re.findall('[^A-Za-z0-9]', password):
        return True
    print('\nPassword does not contain any special characters!')
    return False


def is_in_blacklist(password):
    if password in blacklist:
        print('\nPassword is in blacklist of common passwords!')
        return True
    return False


def is_match_pattern(password):
    patterns = {'phone': '\+?[0-9\-()\s]+',
                'email': '\w+\@\w+\.\w+',
                'date': '([0-9]{1,4}[\\/.\s]?){3}',
                'license plate': '[A-z]{1}[0-9]{3}[A-z]{2}[0-9]{0,3}'}
    for name, pattern in patterns.items():
        pattern = re.compile(pattern)
        if pattern.fullmatch(password):
            print('\nPassword matches common pattern ({0})!'.format(name))
            return True
    return False


def get_password_strength(password):
    score = 10
    if not has_mixed_case(password):
        score -= 2
    if not has_digit(password):
        score -= 2
    if not has_special_chars(password):
        score -= 2
    if is_in_blacklist(password):
        score -= 2
    if is_match_pattern(password):
        score -= 2
    return score


if __name__ == '__main__':
    blacklist = load_blacklist('62kcmnpass.txt')
    if len(sys.argv) > 1:
        password = sys.argv[1]
    else:
        password = input('Input password to check: ')
    score = get_password_strength(password)
    print('\nPassword \'{0}\' got a score of {1}'.format(password, score))
