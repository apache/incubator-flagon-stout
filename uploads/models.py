from django.db import models

class Document(models.Model):
	# DIRECTORY_CHOICES=(
	# 	('exp1', 'exp1'), 
	# 	('exp2', 'exp2'),
	# )
	# directory = models.CharField(max_length=1, choices=DIRECTORY_CHOICES)
	docfile = models.FileField(upload_to='data')
