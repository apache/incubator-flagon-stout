from django.shortcuts import render
from op_tasks.models import UserProfile, Product, Dataset, OpTask, TaskListItem

# Create your views here.

def home_page(request):
	return render(request, 'experimenthome.html')

def view_status(request):
	userprofiles = UserProfile.objects.all()
	products = Product.objects.all()
	tasks = OpTask.objects.all()
	incomplete_tasks = TaskListItem.objects.all().filter(task_complete=False)
	completed_tasks = TaskListItem.objects.all().filter(task_complete=True)
	return render(request, 'status.html', 
		{'userprofiles': userprofiles, 
		'products': products, 
		'tasks': tasks,
		'incomplete_tasks': incomplete_tasks, 
		'completed_tasks': completed_tasks})

def view_products(request):
	products = Product.objects.all()
	return render(request, 'products.html', {'products': products})

def view_users(request):
	userprofiles = UserProfile.objects.all().order_by('-user__last_login')
	return render(request, 'users.html', {'userprofiles': userprofiles})

def view_tasks(request):
	tasks = OpTask.objects.all()
	return render(request, 'tasks.html', {'tasks': tasks})

def view_completed(request):
	completed_tasks = TaskListItem.objects.all().filter(task_complete=True).order_by('-date_complete')
	return render(request, 'completed.html', {'completed_tasks': completed_tasks})

def view_incomplete(request):
	incomplete_tasks = TaskListItem.objects.all().filter(task_complete=False)
	return render(request, 'incomplete.html', {'incomplete_tasks': incomplete_tasks})
	
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