from django.core.urlresolvers import resolve
from django.test import TestCase
from op_tasks.views import instruct

# Create your tests here.

class InstructPageTest(TestCase):
	def test_instruct_url_resolves_to_instruct_page_view(self):
		found=resolve('op_tasks/instruct/')
		self.assertEqual(found.func, instruct)