"""
DJANGO COMMAND TO WAIT FOR DB
"""

from django.core.management.base import BaseCommand
import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError


class Command(BaseCommand):
    """ command to wait for database """

    def handle(self, *args, **options):
        self.stdout.write('waiting for database')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting one second')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('database available'))
