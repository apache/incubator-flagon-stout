from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import make_password

from op_tasks.models import Dataset, Product, OpTask, UserProfile, TaskListItem, Experiment

# Create your tests here.

# class SmokeTest(TestCase):

# 	def test_bad_math(self):
# 		self.assertEqual(1+1,3)

class ModelTest(TestCase):

	def test_user_can_be_assigned_an_experiment(self):
		experiment = Experiment(name='Cow',
			task_count=2,
			task_length=10,
			has_achievements=True,
			has_intake=True,
			has_followup=True,
			auto_tasking=True)
		experiment.save()
		saved_experiments = Experiment.objects.all()
		self.assertEqual(saved_experiments.count(), 1)

		user = User(username='Bob', password=make_password('Bob') )
		user.email = user.username
		user.save()

		saved_users = User.objects.all()
		self.assertEqual(saved_users.count(), 1)

		userprofile = UserProfile()
		userprofile.user = user
		userprofile.experiment = experiment
		userprofile.save()

		saved_profiles = UserProfile.objects.all()
		self.assertEqual(saved_profiles.count(), 1)

		named_experiment = saved_profiles[0].experiment
		self.assertEqual(named_experiment.name, 'Cow')


	def test_saving_and_retrieving_product(self):
		dataset = Dataset()
		dataset.version = '1'
		dataset.name = 'test'

		product = Product()
		product.dataset = dataset
		product.url = 'http://espn.go.com'
		product.team = 'ESPN'
		product.name = 'ESPNews'
		product.version = '1'
		product.instructions = 'http://www.si.com'
		product.save()

		saved_products = Product.objects.all()
		self.assertEqual(saved_products.count(), 1)

		first_product = saved_products[0]
		self.assertEqual(first_product.url, 'http://espn.go.com')
		self.assertEqual(first_product.team, 'ESPN')
		self.assertEqual(first_product.name, 'ESPNews')
		self.assertEqual(first_product.version, '1')
		self.assertEqual(first_product.instructions, 'http://www.si.com')

	def test_saving_and_retrieving_user(self):
		# either of the methods below works...
		user = User(username='Bob', password=make_password('Bob') )
		# user = User()
		# user.username = 'Bob'
		# user.set_password('Bob')
		user.email = user.username
		user.save()

		saved_users = User.objects.all()
		self.assertEqual(saved_users.count(), 1)

		userprofile = UserProfile()
		userprofile.user = user
		userprofile.save()

		saved_profiles = UserProfile.objects.all()
		self.assertEqual(saved_profiles.count(), 1)

		first_profile = saved_profiles[0]
		self.assertEqual(first_profile.user.username, 'Bob')
		self.assertEqual(first_profile.user.username, first_profile.user.email)

	def test_can_get_profile_from_user(self):
		user = User(username='George', password=make_password('George'))
		user.email = user.username
		user.save()

		userprofile = UserProfile(exp_inst_complete=True, portal_inst_complete=True)
		userprofile.user = user 
		userprofile.save()

		saved_user = User.objects.all()[0]
		matched_profile = saved_user.userprofile

		self.assertEqual(userprofile.portal_inst_complete, True)
		self.assertEqual(userprofile.exp_inst_complete, True)
		self.assertEqual(userprofile.task_inst_complete, False)

	def test_can_create_products_and_tasks(self):
		dataset1 = Dataset(name='dataset1', version='1')
		dataset1.save()
		dataset2 = Dataset(name='dataset2', version='1')
		dataset2.save()

		product1 = Product(dataset=dataset1, name='product1', url='111')
		product1.save()
		product2 = Product()
		product2.dataset = dataset2
		product2.name = 'product2'
		product2.url = '222'
		product2.save()

		task1 = OpTask(dataset=dataset1, name='task1')
		task1.save()
		task2 = OpTask(dataset=dataset2, name='task2')
		task2.save()

		saved_products = Product.objects.all()
		first_product = saved_products[0]
		second_product = saved_products[1]

		self.assertEqual(saved_products.count(), 2)
		self.assertNotEqual(first_product.dataset, None)
		self.assertNotEqual(second_product.dataset, None)

	def test_can_match_product_and_task_by_dataset(self):
		dataset1 = Dataset(name='dataset1', version='1')
		dataset1.save()
		dataset2 = Dataset(name='dataset2', version='1')
		dataset2.save()

		product1 = Product(dataset=dataset1, name='product1', url='111')
		product1.save()
		product2 = Product()
		product2.dataset = dataset2
		product2.name = 'product2'
		product2.url = '222'
		product2.save()

		task1 = OpTask(dataset=dataset1, name='task1')
		task1.save()
		task2 = OpTask(dataset=dataset2, name='task2')
		task2.save()

		saved_products = Product.objects.all()
		first_product = saved_products[0]
		first_dataset = first_product.dataset
		second_product = saved_products[1]
		second_dataset = second_product.dataset

		first_matched_tasks = first_dataset.optask_set.all()
		first_task = first_matched_tasks[0]
		second_matched_tasks = second_dataset.optask_set.all()
		second_task = second_matched_tasks[0]

		self.assertEqual(first_product.dataset, first_task.dataset)
		self.assertEqual(second_product.dataset, second_task.dataset)

	def test_can_find_users_tasks(self):
		# create a bunch of users
		user1 = User(username='John', password=make_password('John'))
		user1.save()
		userprofile1 = UserProfile(user=user1)
		userprofile1.save()

		user2 = User(username='Paul', password=make_password('Paul'))
		user2.save()
		userprofile2 = UserProfile(user=user2)
		userprofile2.save()

		user3 = User(username='Ringo', password=make_password('Ringo'))
		user3.save()
		userprofile3 = UserProfile(user=user3)
		userprofile3.save()

		# assign them some tasks 
		testdata = Dataset(name='testdata', version='1')
		testdata.save()

		testproduct = Product(dataset=testdata, name='testproduct', url='testproduct')
		testproduct.save()

		testtask1 = OpTask(dataset=testdata, name='task1')
		testtask1.save()
		testtask2 = OpTask(dataset=testdata, name='task2')
		testtask2.save()

		test_tli_1 = TaskListItem(userprofile=userprofile1, product=testproduct, op_task=testtask1, index=0)
		test_tli_1.save()
		test_tli_2 = TaskListItem(userprofile=userprofile1, product=testproduct, op_task=testtask2, index=1)
		test_tli_2.save()

		test_tlis = TaskListItem.objects.all()
		self.assertEqual(test_tlis.count(),2)

		# find the matches based on user profiles 
		saved_userprofiles = UserProfile.objects.all()
		for userprofile in saved_userprofiles:
			matched_task_items = userprofile.tasklistitem_set.all()
			if userprofile.user.username == 'John':
				self.assertEqual(matched_task_items.count(),2)
			else:
				self.assertEqual(matched_task_items.count(),0)