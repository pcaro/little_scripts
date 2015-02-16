#!/usr/bin/env python
## -*- coding: utf8 -*-


def get_password():
    import random
    # Make a list of all of the words in our system dictionary
    # sudo zypper in dicts
    f = open('/usr/src/dicts/espa~nol-1.5/espa~nol.words')
    # f = open('/usr/share/dict/words')
    words = [x.strip() for x in f.readlines()]
    # Pick 2 random words from the list
    password = '-'.join(random.choice(words) for i in range(2))
    # Remove any apostrophes
    password = password.replace("'", '')
    # Add a random number to the end of our password
    password += '-'
    number1 = str(random.randint(1, 10))
    number2 = str(random.randint(1, 10))
    password += number1 + number1 + number2 + number2
    return password

if __name__ == '__main__':
    for _ in range(5):
        print get_password()
