from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from op_tasks.models import *
import os

class Command(BaseCommand):    
    help = 'our help string comes here'

    def _reset(self):
    	os.system('python manage.py sqlclear op_tasks | python manage.py dbshell')
    	os.system('python manage.py syncdb')
    	os.system('python manage.py populate_db')

    def handle(self, *args, **options):
        self._reset()