from django.shortcuts import render, redirect
from op_tasks.models import UserProfile, Product, Dataset, OpTask, TaskListItem, Experiment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from users import *
from products import *
from tasks import *
from email import *
import csv
import pandas

@login_required(login_url='/tasking/login')
def home_page(request):
	return render(request, 'experimenthome.html')


@login_required(login_url='/tasking/login')
def view_status(request):
	experiments = Experiment.objects.all()
	masterList = {}
	for experiment in experiments:
		name = experiment.name
		userprofiles = experiment.userprofile_set.all()
		usp = sorted(userprofiles)
		products = []
		tasks = []
		completedTasks = []
		incompleteTasks = []
		experimentList = {}
		for userprofile in userprofiles:
			tasklistitems = userprofile.tasklistitem_set.all()
			for tasklistitem in tasklistitems:
				products.append(tasklistitem.product)
				tasks.append(tasklistitem.op_task)
				if tasklistitem.task_complete is True:
					completedTasks.append(tasklistitem)
				else:
					incompleteTasks.append(tasklistitem)
		percentageComplete = int((len(completedTasks) / float(len(completedTasks) + len(incompleteTasks))) * 100)
		sortedProd = sorted(set(products))
		sortedTasks = sorted(set(tasks))
		sortedCompletedTasks = sorted(completedTasks)
		sortedIncompleteTasks = sorted(incompleteTasks)
		experimentList["users"] = usp
		experimentList["products"] = sortedProd
		experimentList["tasks"] = sortedTasks
		experimentList["completedTasks"] = sortedCompletedTasks
		experimentList["incompleteTasks"] = sortedIncompleteTasks
		experimentList["percentageComplete"] = percentageComplete
		masterList[name] = experimentList
	return render(request, 'status.html', {'experimentList': masterList})	


@login_required(login_url='/tasking/login')
def manage_exps(request):
	experimentlist = Experiment.objects.all()
	return render(request, 'experiments.html', {'experimentlist': experimentlist})


@login_required(login_url='/tasking/login')
def view_exp_details(request, exppk):
	experiment = Experiment.objects.get(id=exppk)
	return render(request, 'experiment_details.html', {'experiment':experiment})


@login_required(login_url='/tasking/login')
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


@login_required(login_url='/tasking/login')
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


@login_required(login_url='/tasking/login')
def manage_datasets(request):
	datasets = Dataset.objects.all()
	return render(request, 'datasets.html', {'datasets':datasets})


@login_required(login_url='/tasking/login')
def view_dataset_details(request, datasetpk):
	dataset = Dataset.objects.get(id=datasetpk)
	return render(request, 'dataset_details.html', {'dataset':dataset})


@login_required(login_url='/tasking/login')
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


@login_required(login_url='/tasking/login')
def edit_dataset(request, datasetpk):
	dataset = Dataset.objects.get(id=datasetpk)
	dataset.name = request.POST['dataset_name']
	dataset.version = request.POST['dataset_version']
	dataset.is_active = request.POST.get('dataset_active', False)

	dataset.save()

	return redirect('exp_portal:manage_datasets')


@login_required(login_url='/tasking/login')
def view_experiment_products(request):
	experiments = Experiment.objects.all()
	masterList = {}
	for experiment in experiments:
		name = experiment.name
		userprofiles = experiment.userprofile_set.all()
		usp = sorted(userprofiles)
		products = []
		tasks = []
		completedTasks = []
		incompleteTasks = []
		experimentList = {}
		for userprofile in userprofiles:
			tasklistitems = userprofile.tasklistitem_set.all()
			for tasklistitem in tasklistitems:
				products.append(tasklistitem.product)
				tasks.append(tasklistitem.op_task)
				if tasklistitem.task_complete is True:
					completedTasks.append(tasklistitem)
				else:
					incompleteTasks.append(tasklistitem)
		percentageComplete = int((len(completedTasks) / float(len(completedTasks) + len(incompleteTasks))) * 100)
		sortedProd = sorted(set(products))
		sortedTasks = sorted(set(tasks))
		sortedCompletedTasks = sorted(completedTasks)
		sortedIncompleteTasks = sorted(incompleteTasks)
		experimentList["users"] = usp
		experimentList["products"] = sortedProd
		experimentList["tasks"] = sortedTasks
		experimentList["completedTasks"] = sortedCompletedTasks
		experimentList["incompleteTasks"] = sortedIncompleteTasks
		experimentList["percentageComplete"] = percentageComplete
		masterList[name] = experimentList
	response = JsonResponse({'experimentInfo': str(masterList)})
	return response