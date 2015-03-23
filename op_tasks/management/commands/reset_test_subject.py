from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from op_tasks.models import UserProfile, TaskListItem
import os

class Command(BaseCommand):    
    help = 'our help string comes here'

    def _reset(self):
    	saved_users = User.objects.all()

    def handle(self, *args, **options):
        self._reset()