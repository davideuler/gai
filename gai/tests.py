import random

from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson as json

from gai.base56 import (
     mmi_hash,
     mmi_unhash
)
from gai.settings import (
    PRIMES,
    PRIME_MMIS
)

class Base56Test(TestCase):

    def test_primes(self):
        """
        Tests that prime * mmi % 56 ^ n equals 1
        """
        for i in xrange(1, len(PRIMES)):
            self.assertEqual((PRIMES[i] * PRIME_MMIS[i]) % 56 ** i, 1)

    def test_hash(self):
        """
        Tests that hash function is a bijection
        """
        for i in xrange(len(PRIMES)-1):
            num = 56 ** i + random.randint(1, 50)
            self.assertEqual(mmi_unhash(mmi_hash(num)), num)


class ShortenTest(TestCase):

    def test_shorten(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        url = '/a/shorten'
        to_shorten = 'http://www.example.com/'
        r = c.post(url, {'origin': ''})
        self.assertEqual(r.status_code, 400)
        r = c.post(url, {'origin': 'abc'})
        self.assertEqual(r.status_code, 400)
        r = c.post(url, {'origin': to_shorten})
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)
        r = c.get('/%s' % data['shorten'], follow=True)
        self.assertEqual(r.redirect_chain[0][0], to_shorten)
