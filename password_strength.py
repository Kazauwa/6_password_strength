import sys
import re
from getpass import getpass


def load_blacklist(path):
    with open(path, 'r') as reader:
        blacklist = reader.read()
    blacklist = re.split('\s+', blacklist)
    return blacklist


def has_mixed_case(password):
    """Mixed case (e.g. 'PassWord')"""
    if not password.isupper() and not password.islower():
        return True
    return False


def has_digit(password):
    """Digit inclusion (e.g. 'password123')"""
    if re.findall('\d+', password):
        return True
    return False


def has_special_chars(password):
    """Special char inclusion (e.g. 'p@$$word')"""
    if re.findall('[^A-Za-z0-9]', password):
        return True
    return False


def not_in_blacklist(password):
    """Blacklist test (if password is in list of frequently-used passwords)"""
    if not blacklist:
        return True
    if password in blacklist:
        return False
    return True


def not_match_pattern(password):
    """Pattern match rule (e.g. if password is number, date or email)"""
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
    failed_tests = list()
    score = 10
    for test in tests_list:
        if not test(password):
            score -= 2
            failed_tests.append(test.__doc__)
    return score, failed_tests


tests_list = [has_mixed_case,
              has_digit,
              has_special_chars,
              not_in_blacklist,
              not_match_pattern]

if __name__ == '__main__':
    try:
        blacklist = load_blacklist(sys.argv[1])
    except IndexError:
        blacklist = None
    password = getpass('Input a password to check: ')
    score, failed_tests = get_password_strength(password)
    print('\nYour password got a score of {0}'.format(score))
    if score < 10:
        print('\nFailed tests:\n')
    for test in failed_tests:
        print('* {}'.format(test))
