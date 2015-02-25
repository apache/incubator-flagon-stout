from django.test import TestCase
from op_tasks.models import Participant, Product, Dataset, OpTask

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
		