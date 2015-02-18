from django.core.urlresolvers import resolve
from django.test import TestCase
from op_tasks.views import instruct
from op_tasks.models import Dataset, Product

# Create your tests here.

# class SmokeTest(TestCase):

# 	def test_bad_math(self):
# 		self.assertEqual(1+1,3)

class ProductModelTest(TestCase):

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

		saved_product = Product.objects.all()
		self.assertEqual(saved_product.count(), 1)