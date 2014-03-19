from unittest import TestCase

from django.core.exceptions import ValidationError
from nose_parameterized import parameterized

from oracle.forms import validate_collectors_number


class CollectorNumberTest(TestCase):
    @parameterized.expand([
        ('123a', 123, 'a'),
        ('123', 123, None),
        ('foo', None, None),
    ])
    def test_number_parse(self, raw, number, sub_number):
        self.assertEqual(validate_collectors_number(raw), (number, sub_number))

    def test_validation_exception_for_required(self):
        with self.assertRaises(ValidationError):
            validate_collectors_number('foo', required=True)
