# reset datetime stamps to make them aware and not naive

from django.core.management.base import BaseCommand
import datetime
import pytz

from op_tasks.models import Dataset, Product, OpTask, UserProfile, TaskListItem

class Command(BaseCommand):
	def update_time(self):
		saved_task_items = TaskListItem.objects.all()
		for saved_task_item in saved_task_items:
			unaware = saved_task_item.date_complete
			now_aware = pytz.utc.localize(unaware)
			saved_task_item.datetime = now_aware
			saved_task_item.save()

	def handle(self, *args, **options):
		self.update_time()