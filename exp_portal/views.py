from django.shortcuts import render
from op_tasks.models import UserProfile, Product, Dataset, OpTask, TaskListItem

# Create your views here.

def home_page(request):
	return render(request, 'experimenthome.html')

def view_status(request):
	userprofiles = UserProfile.objects.all()
	products = Product.objects.all()
	datasets = Dataset.objects.all()
	optasks = OpTask.objects.all()
	tasklistitems = TaskListItem.objects.all()
	return render(request, 'status.html', {'userprofiles': userprofiles, 'products': products, 'datasets': datasets,'optasks': optasks, 'tasklistitems': tasklistitems})

def view_products(request):
	products = Product.objects.all()
	return render(request, 'products.html', {'products': products})

def submit_task(request):
	return render(request, 'submit_task.html')

def new_task(request):
	dataset = Dataset.objects.create(name=request.POST['task_dataset'])
	OpTask.objects.create(dataset=dataset, 
		survey_url=request.POST['task_url'], 
		name=request.POST['task_name'], 
		instructions=request.POST['task_instructions'], 
		is_active=request.POST['active_check'])
	return redirect('/experiment/taskAdded/')

def task_added(request):
	return render(request, 'task_added.html')