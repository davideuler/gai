from gai.settings import (
    CHARSET,
    MIN_LENGTH,
    PRIMES,
    PRIME_MMIS
)

def base56_encode(num):
    encoded = ""
    while num > 0:
        mod = num % 56
        encoded += CHARSET[mod]
        num = num / 56
    return encoded


def base56_decode(encoded):
    num = 0
    i = 0
    for char in encoded:
        dec = CHARSET.index(char)
        num += dec * 56 ** i
        i += 1
    return num


def mmi_hash(num):
    length = 0
    for order in xrange(len(PRIMES)):
        length = order
        if num < 56 ** order:
            break
    if length < MIN_LENGTH:
        length = MIN_LENGTH
    ceil = pow(56, length)
    dec = (num * PRIMES[length]) % ceil
    return base56_encode(dec).zfill(length)


def mmi_unhash(hash):
    ceil = pow(56, len(hash))
    num = base56_decode(hash.strip('0'))
    dec = (num * PRIME_MMIS[len(hash)]) % ceil
    return dec
