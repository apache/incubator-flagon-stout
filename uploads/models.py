from django.db import models

def content_file_name(request, filename):
	return '/'.join([request.POST['dirName'], filename])

class Document(models.Model):
	dirPath = models.CharField(max_length=1000, default="abc")
	docfile = models.FileField(upload_to=content_file_name)
