import math
import sys
BASE = 62

DIGIT_OFFSET = 48
UPPERCASE_OFFSET = 55
LOWERCASE_OFFSET = 61

def true_chr(integer):
    if integer < 10:
        return chr(integer + DIGIT_OFFSET)
    elif 10 <= integer <= 35:
        return chr(integer + UPPERCASE_OFFSET)
    elif 36 <= integer < 62:
        return chr(integer + LOWERCASE_OFFSET)
    else:
        raise ValueError("%d is not a valid integer in the range of base %d" % (integer, BASE))

def shorten_url(integer):
    if integer == 0:
        return '0'

    short = ""
    while integer > 0:
        remainder = integer % BASE

        short = true_chr(int(remainder)) + short
        integer /= BASE
        integer = int(integer)

    return short

