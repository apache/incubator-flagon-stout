from django.shortcuts import render
from op_tasks.models import Participant, Product, Dataset, OpTask

# Create your views here.

def view_status(request):
	participants = Participant.objects.all()
	products = Product.objects.all()
	datasets = Dataset.objects.all()
	optasks = OpTask.objects.all()
	return render(request, 'exp_status.html', {'participants': participants, 'products': products, 'datasets': datasets,'optasks': optasks})