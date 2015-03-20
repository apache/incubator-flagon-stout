from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Chrome()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.close()

	def test_can_register_and_navigate_to_task_list(self):
		# browse to online portal
		self.browser.get(self.live_server_url)

		# click the sign in page
		self.browser.find_element_by_link_text("Register").click()

		# click to accept the intro material
		self.browser.find_element_by_id("intro-complete").submit()

		# register a new user
		inputemail = self.browser.find_element_by_name("email")
		inputpassword = self.browser.find_element_by_name("password")
		inputemail.send_keys("dftnew@test.com")
		inputpassword.send_keys("dft")
		self.browser.find_element_by_name("submit").submit()
		self.browser.implicitly_wait(5)

