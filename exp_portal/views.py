from django.shortcuts import render, redirect
from op_tasks.models import UserProfile, Product, Dataset, OpTask, TaskListItem, Experiment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url='/tasking/login')
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

def manage_products(request):
	products = Product.objects.all()
	return render(request, 'products.html', {'products': products})

def view_users(request):
	userprofiles = UserProfile.objects.all().order_by('-user__last_login')
	return render(request, 'users.html', {'userprofiles': userprofiles})

def manage_users(request):
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
	
def add_task(request):
	datasets = Dataset.objects.all()
	return render(request, 'add_task.html', {'datasets': datasets})

def new_task(request):
	dataset = Dataset.objects.all().filter(name=request.POST['task_dataset'])[0]
	OpTask.objects.create(dataset=dataset, 
		survey_url=request.POST['task_url'], 
		name=request.POST['task_name'], 
		instructions=request.POST['task_instructions']#, 
		# is_active=request.POST['active_check']
		)
	return redirect('/experiment/tasks/submit')

def task_added(request):
	return render(request, 'task_added.html')

def manage_tasks(request):
	return view_tasks(request)

def add_user(request):
	experiments = Experiment.objects.all()
	return render(request, 'add_user.html', {'experiments': experiments})

def new_user(request):
	# add logic to create participant
	user = User(username=request.POST['username'])
	user.set_password(request.POST['password_1'])
	user.email = user.username
	user.save()

	userprofile = UserProfile()
	userprofile.user = user
	experiment = Experiment.objects.all().filter(name=request.POST['experiment_name'])[0]
	userprofile.experiment = experiment
	userprofile.save()

	return view_users(request)

def user_added(request):
	return render(request, 'user_added.html')

def view_user_tasks(request, profile):
	return render(request, 'user_tasks.html')