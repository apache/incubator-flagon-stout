from django.shortcuts import render, redirect
from op_tasks.models import UserProfile, Product, Dataset, OpTask, TaskListItem, Experiment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users import *
from products import *
from tasks import *
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
