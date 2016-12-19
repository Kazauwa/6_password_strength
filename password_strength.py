import sys
import re
from getpass import getpass


def load_blacklist(path):
    with open(path, 'r') as reader:
        blacklist = reader.read()
    blacklist = re.split('\s+', blacklist)
    return blacklist


def has_mixed_case(password):
    return not password.isupper() and not password.islower()


def has_digit(password):
    return bool(re.findall('\d+', password))


def has_special_chars(password):
    return bool(re.findall('[^A-Za-z0-9]', password))


def not_in_blacklist(password):
    return password not in blacklist if blacklist else True


def not_match_pattern(password):
    patterns = {'phone': '\+?[0-9\-()\s]+',
                'email': '\w+\@\w+\.\w+',
                'date': '([0-9]{1,4}[\\/.\s]?){3}',
                'license plate': '[A-z]{1}[0-9]{3}[A-z]{2}[0-9]{0,3}'}
    for name, pattern in patterns.items():
        pattern = re.compile(pattern)
        if pattern.fullmatch(password):
            return False
    return True


def get_password_strength(password):
    score = 0
    score += has_mixed_case(password) * 2
    score += has_digit(password) * 2
    score += has_special_chars(password) * 2
    score += not_in_blacklist(password) * 2
    score += not_match_pattern(password) * 2
    return score


if __name__ == '__main__':
    try:
        blacklist = load_blacklist(sys.argv[1])
    except IndexError:
        blacklist = None
    password = getpass('Input a password to check: ')
    score = get_password_strength(password)
    print('Your password got a score of {}/10'.format(score))
