from django.test import TestCase
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from op_tasks.models import Product, Dataset, OpTask, TaskListItem, UserProfile

# Create your tests here.

class ExperimentTest(TestCase):

	def test_can_add_and_retrieve_database_items(self):
		dataset = Dataset()
		dataset.version = '1'
		dataset.name = 'test'
		dataset.save()

		product = Product()
		product.dataset = dataset
		product.url = 'http://www.cnn.com'
		product.team = 'CNN'
		product.name = 'CNN News'
		product.version = '1'
		product.instructions = 'http://www.cnn.com'
		product.save()

		saved_products = Product.objects.all()
		self.assertEqual(saved_products.count(),1)

	def test_can_count_completed_tasks(self):
		dataset = Dataset(version='1', name='test')
		dataset.save()

		task = OpTask(dataset=dataset, name='test_task', survey_url='test_url')
		task.save()

		user = User(username='john', password=make_password('paul'))
		user.save()

		userprofile = UserProfile(user=user)
		userprofile.save()

		product = Product(dataset=dataset, url='test_url')
		product.save()

		TaskListItem(
			userprofile=userprofile, 
			op_task=task,
			product=product,
			index=0,
			task_active=True,
			task_complete=False,
			exit_active=False,
			exit_complete=False).save()

		TaskListItem(
			userprofile=userprofile,
			op_task=task,
			product=product,
			index=1,
			task_active=False,
			task_complete=True,
			exit_active=False,
			exit_complete=False).save()

		saved_tasks = TaskListItem.objects.all()
		self.assertEqual(saved_tasks.count(), 2)

		self.assertEqual(saved_tasks.filter(task_active=True).count(), 1)
		self.assertEqual(saved_tasks.filter(task_complete=False).count(), 1)