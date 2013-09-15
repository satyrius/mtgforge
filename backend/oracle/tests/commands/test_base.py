# -*- coding: utf-8 -*-

from mock import patch
from django.test import TestCase
from oracle.management.base import BaseCommand


class BaseCommandTest(TestCase):
    @patch('sys.stdout')
    def test_notice_message(self, stdout):
        class Command(BaseCommand):
            def handle(self, *args, **options):
                self.notice('asd')
                self.notice(u'йцукен')
                self.notice('\xc3\x86')

        Command().execute()
        self.assertEqual(stdout.write.call_count, 3)

    @patch('sys.stderr')
    def test_error_message(self, stderr):
        class Command(BaseCommand):
            def handle(self, *args, **options):
                self.error('asd')
                self.error(u'йцукен')
                self.error('\xc3\x86')

        Command().execute()
        self.assertEqual(stderr.write.call_count, 3)
