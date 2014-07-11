from django.core.management.base import BaseCommand
from op_tasks.models import *

class Command(BaseCommand):    
    help = 'our help string comes here'

    def _create_data(self):
    	Data(name='Kiva').save()

    def handle(self, *args, **options):
        self._create_data()