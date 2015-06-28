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

def view_product_details(request, productname):
	product = Product.objects.all().filter(name=productname)[0]
	datasets = Dataset.objects.all()
	return render(request, 'product_details.html', {'product': product, 'datasets': datasets})

def edit_product(request, productpk):
	product = Product.objects.get(id=productpk)
	product.name = request.POST['product_name']
	product.team = request.POST['product_team']
	product.url = request.POST['product_url']
	product.instructions = request.POST['instructions_url']
	product.version = request.POST['version']
	product.is_active = request.POST.get('is_active', False)

	# TODO error checking on this, though it should never fail 
	dataset = Dataset.objects.all().filter(name=request.POST['dataset'])[0]
	product.dataset = dataset

	product.save()

	return redirect('exp_portal:view_products')

def manage_products(request):
	products = Product.objects.all()
	return render(request, 'products.html', {'products': products})

def add_product(request):
	datasets = Dataset.objects.all()
	return render(request, 'add_product.html', {'datasets': datasets})

def new_product(request):
	product = Product(name=request.POST['product_name'])
	product.url = request.POST['product_url']
	product.team = request.POST['product_team']
	product.url = request.POST['product_url']
	product.version = request.POST['product_version']
	product.instructions = request.POST['product_instructions']
	product.is_active = request.POST.get('product_active', False)

	dataset = Dataset.objects.get(name=request.POST['product_dataset'])

	product.save()

	return redirect('exp_portal:view_products')

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
	dataset = Dataset.objects.get(name=request.POST['task_dataset'])
	task = OpTask()
	task.dataset = dataset
	task.survey_url = request.POST['task_url']
	task.name = request.POST['task_name']
	task.instructions = request.POST['task_instructions']
	task.exit_url = request.POST['task_exit_url']

	task.save()
	return redirect('exp_portal:view_tasks')

def manage_tasks(request):
	return view_tasks(request)

def view_task_details(request, taskname):
	task = OpTask.objects.all().filter(name=taskname)[0]
	datasets = Dataset.objects.all()
	print task.dataset.name
	for dataset in datasets:
		print dataset.name
	return render(request, 'task_details.html', {'task': task, 'datasets': datasets})

def edit_task(request, taskpk):
	task = OpTask.objects.get(id=taskpk)
	task.name = request.POST['task_name']
	task.survey_url = request.POST['task_url']
	task.exit_url = request.POST['task_exit_url']
	task.instructions =request.POST['task_instructions']

	dataset = Dataset.objects.get(name=request.POST['task_dataset'])
	task.dataset = dataset

	task.is_active = request.POST.get('task_active', False)

	task.save()

	return redirect('exp_portal:view_tasks')

def add_user(request):
	experiments = Experiment.objects.all()
	products = Product.objects.all()
	return render(request, 'add_user.html', {'experiments': experiments, 'products':products})

def new_user(request):
	user = User(username=request.POST['username'])
	user.set_password(request.POST['password_1'])
	user.email = user.username
	user.save()

	userprofile = UserProfile()
	userprofile.user = user
	experiment = Experiment.objects.get(name=request.POST['experiment_name'])
	userprofile.experiment = experiment
	userprofile.save()

	# logic for assigning tasks
	if request.POST['product_name'] == 'all':
		# set to assign all tasks
		# TBD update to reflect experiment settings
		index = 0
		datasets = Dataset.objects.all()
		for dataset in datasets:
			products = dataset.product_set.all()
			for product in products:
				tasks = dataset.optask_set.all()
				for task in tasks:
					newtasklistitem = TaskListItem()
					newtasklistitem.userprofile = userprofile
					newtasklistitem.op_task = task
					newtasklistitem.product = product
					newtasklistitem.index = index
					index = index + 1
					newtasklistitem.task_active = True
					newtasklistitem.save()
	else:
		product = Product.objects.get(name=request.POST['product_name'])
		if str(request.POST['taskorder']) == 'b':
			print 'true'
			tasks = product.dataset.optask_set.all().order_by('id').reverse()
		else:
			tasks = product.dataset.optask_set.all().order_by('id')

		index = 0
		for task in tasks:
			newtasklistitem = TaskListItem()
			newtasklistitem.userprofile = userprofile
			newtasklistitem.op_task = task
			newtasklistitem.product = product
			newtasklistitem.index = index
			if index == 0 or experiment.sequential_tasks == False:
				newtasklistitem.task_active = True
			else:
				newtasklistitem.task_active = False
			index = index + 1
			newtasklistitem.save()


	return redirect('exp_portal:view_users')

def user_added(request):
	return render(request, 'user_added.html')

def view_user_tasks(request, profile):
	userprofile = UserProfile.objects.all().filter(user_hash=profile)[0]
	usertasks = userprofile.tasklistitem_set.all()
	
	datasets = Dataset.objects.all()
	count = 0
	tasklistitems = []
	for dataset in datasets:
		for product in dataset.product_set.all():
			for task in dataset.optask_set.all():
				count = count + 1

	return render(request, 'user_tasks.html', {'userprofile': userprofile})

def add_user_task(request, userpk):
	userprofile = UserProfile.objects.get(id=userpk)
	datasets = Dataset.objects.all()
	products = Product.objects.all()
	tasks = OpTask.objects.all()
	return render(request, 'add_user_task.html', {'userprofile':userprofile, 
		'datasets': datasets, 'products': products, 'tasks': tasks})

def update_user_tasks(request, userpk, datasetpk, productpk, taskpk):
	dataset = Dataset.objects.get(id=datasetpk)
	userprofile = UserProfile.objects.get(id=userpk)
	index = userprofile.tasklistitem_set.count()

	newtasklistitem = TaskListItem()
	newtasklistitem.userprofile = userprofile
	newtasklistitem.op_task = OpTask.objects.get(id=taskpk)
	newtasklistitem.product = Product.objects.get(id=productpk)
	newtasklistitem.index = index
	newtasklistitem.task_active = True
	newtasklistitem.save()

	return redirect('exp_portal:add_user_task', userpk)

def manage_exps(request):
	experimentlist = Experiment.objects.all()
	return render(request, 'experiments.html', {'experimentlist': experimentlist})

def view_exp_details(request, exppk):
	experiment = Experiment.objects.get(id=exppk)
	return render(request, 'experiment_details.html', {'experiment':experiment})

def add_exp(request):
	if request.method == 'POST':
		experiment = Experiment()
		experiment.name = request.POST['exp_name']
		experiment.task_count = request.POST['exp_taskcount']
		experiment.task_length = request.POST['exp_tasklength']
		experiment.has_achievements = request.POST.get('exp_achievements', False)
		experiment.has_intake = request.POST.get('exp_intake', False)
		experiment.has_followup = request.POST.get('exp_followup', False)
		experiment.consent = request.POST.get('exp_consent', False)
		experiment.sequential_tasks = request.POST.get('exp_sequentialtasks', False)
		experiment.show_progress = request.POST.get('exp_progress', False)
		experiment.timed = request.POST.get('exp_timed', False)

		experiment.save()
		return redirect('exp_portal:manage_exps')

	return render(request, 'add_experiment.html')

def edit_exp(request, exppk):
	experiment = Experiment.objects.get(id=exppk)
	experiment.name = request.POST['exp_name']
	experiment.task_count = request.POST['exp_taskcount']
	experiment.task_length = request.POST['exp_tasklength']
	experiment.has_achievements = request.POST.get('exp_achievements', False)
	experiment.has_intake = request.POST.get('exp_intake', False)
	experiment.has_followup = request.POST.get('exp_followup', False)
	experiment.consent = request.POST.get('exp_consent', False)
	experiment.sequential_tasks = request.POST.get('exp_sequentialtasks', False)
	experiment.show_progress = request.POST.get('exp_progress', False)
	experiment.timed = request.POST.get('exp_timed', False)

	experiment.save()

	return redirect('exp_portal:manage_exps')

def manage_datasets(request):
	datasets = Dataset.objects.all()
	return render(request, 'datasets.html', {'datasets':datasets})

def view_dataset_details(request, datasetpk):
	dataset = Dataset.objects.get(id=datasetpk)
	return render(request, 'dataset_details.html', {'dataset':dataset})

def add_dataset(request):
	if request.method == 'POST':
		# do update
		dataset = Dataset()
		dataset.name = request.POST['dataset_name']
		dataset.version = request.POST['dataset_version']
		dataset.is_active = request.POST.get('dataset_active', False)

		dataset.save()
		return redirect('exp_portal:manage_datasets')
	# else fall here
	return render(request, 'add_dataset.html')

def edit_dataset(request, datasetpk):
	dataset = Dataset.objects.get(id=datasetpk)
	dataset.name = request.POST['dataset_name']
	dataset.version = request.POST['dataset_version']
	dataset.is_active = request.POST.get('dataset_active', False)

	dataset.save()

	return redirect('exp_portal:manage_datasets')
