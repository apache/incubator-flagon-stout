from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
import sys

from op_tasks.models import Dataset, Product, OpTask, UserProfile, TaskListItem, Experiment

import os
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:9000-9200'

class NewVisitorTest(LiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				return
			super(NewVisitorTest, cls).setUpClass()
			cls.server_url = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super(NewVisitorTest, cls).tearDownClass()

	def setUp(self):
		# REALLY REALLY should do this soon...
		# TODO find a way to call populate_db
		experiment = Experiment(name='Test-exp', 
			task_count=2, 
			task_length=30, 
			has_achievements=True, 
			has_intake=True, 
			has_followup=True, 
			auto_tasking=True)
		experiment.save()

		test_tasks =  [
		{'name': 'Functional-Test-OT1',
		'ot_survey_url': 'https://www.surveymonkey.com/s/LR37HZG',
		'ot_exit_url': 'https://www.surveymonkey.com/s/VD8NQZT'},
		{'name': 'Functional-Test-OT2',
		'ot_survey_url': 'https://www.surveymonkey.com/s/LR37HZG',
		'ot_exit_url': 'https://www.surveymonkey.com/s/VD8NQZT'}]

		dataset = Dataset(name='Functional-Test-DS', version='v0.1')
		dataset.save()

		Product(dataset=dataset, 
            url='/static/testing/index.html', 
            instructions=settings.STATIC_URL + 'testing/instructions.html', 
            team='functional-test-team', 
			name='functional-test-product',
			version='v0.1').save()

		for task in test_tasks:
			newtask = OpTask(dataset=dataset,
				name=task['name'],
				survey_url=task['ot_survey_url'],
				exit_url=task['ot_exit_url']).save()

		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.close()

	def test_can_register_a_user_with_tasks(self):
		# browse to online portal
		self.browser.get(self.server_url)

		# check the title of the webpage 
		self.assertIn('XDATA', self.browser.title)

		# click the sign in page
		self.browser.find_element_by_link_text("Register").click()

		# click to accept the intro material
		self.browser.find_element_by_id("intro-complete").submit()

		# register a new user
		inputemail = self.browser.find_element_by_name("username")
		inputemail.send_keys("new@test.com")

		inputpassword = self.browser.find_element_by_name("password")
		inputpassword.send_keys("new")
		
		inputpassword2 = self.browser.find_element_by_name("password2")
		inputpassword2.send_keys("new")

		register_button = self.browser.find_element_by_id("id_register_button")
		register_button.click()

		# check successful registration
		saved_users = User.objects.all()
		self.assertEqual(saved_users.count(), 1)
		self.assertEqual(saved_users[0].username, 'new@test.com')

		saved_products = Product.objects.all()
		self.assertEqual(saved_products.count(), 1)
		self.assertEqual(saved_products[0].team, 'functional-test-team')

		saved_task_list_items = TaskListItem.objects.all()
		self.assertEqual(saved_task_list_items.count(), 2)
		first_task = saved_task_list_items[0]
		second_task = saved_task_list_items[1]
		self.assertEqual(first_task.userprofile, second_task.userprofile)
		self.assertEqual(first_task.userprofile.user.username, 'new@test.com')
		self.assertEqual(second_task.userprofile.user.username, 'new@test.com')

	# def test_can_show_STOUT_and_ALE_integration(self):
		# experiment admin page load showing experiment setup
		# what does experiment setup process look like?

		# user registers and browses to task list
		# completes first part of experiment

		# browse back to experiment admin page to show results