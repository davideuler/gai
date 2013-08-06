# -*- coding: utf-8 -*-
# Minimium length of shortened url
# Must be larger than 2
MIN_LENGTH = 2

# Generated by shuffling the set of 56 chars,
# A-Za-z0-9 except I, l, 1, o, O and 0 that may be ambiguous
# in some fonts, namely
# 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789'
# Don't share it with anybody.
CHARSET = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789'

# Some primes greater than 56 ^ n / 1.61803398874989484
PRIMES = (1, 41, 2377, 147299, 9132313, 566201239, 35104476161, 2176477521929,
          134941606358731, 8366379594239857, 518715534842869223)

# Modular multiplicative inverses of the primes above a modulo 56 ^ n
PRIME_MMIS = (0, 41, 1913, 138827, 8332073, 245539879, 30024414209,
              1027858277945, 218295060195, 4497555361599889,
              110048532750208471)

SITE_TITLE = u'垓'

SITE_SUBTITLE = u'Gai = 10<sup>20</sup>'