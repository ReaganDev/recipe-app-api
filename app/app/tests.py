

from django.test import SimpleTestCase
from .calc import addition, subtraction


class CalcTests(SimpleTestCase):

    def test_addTest(self):
        res = addition(7, 5)

        self.assertEqual(res, 12)

    def test_subtract(self):
        res = subtraction(9, 5)

        self.assertEqual(res, 4)
