import json
import os.path

from django.shortcuts import render, redirect
from op_tasks.models import UserProfile, Product, Dataset, OpTask, TaskListItem, Experiment
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from users import *
from products import *
from tasks import *
from email import *


def user_authorized(request):
	user = request.user
	return user.is_staff


@login_required(login_url='/tasking/login')
def home_page(request):
	if user_authorized(request):
		return render(request, 'experimenthome.html')

@csrf_protect
@login_required(login_url='/tasking/login')
def metrics_data(request):
	rparams = json.loads(request.body)
	if request.method == 'POST':
		experiment = rparams['experiment']
		category = rparams['category']
		tool = rparams['tool']
		task = rparams['task']
		# load experiment data from file
		histDataFile = "/home/ubuntu/SCOtCH/"+experiment+".json"
		histDataAll = []
		if os.path.isfile(histDataFile):
			with open(histDataFile) as data_file:
				histDataAll = json.load(data_file)
		# filter experiment data
		histData = []
		for row in histDataAll:
			if (tool!="all" and tool!=row['SYS.FIL.APP.']) or (task!="all" and task!=row['SYS.FIL.TSK.']):
				continue
			if category=="Load":
				if row['PST.EXP.CLD.'] != "NA" and row['PST.EXP.CLD.'] != "NaN":
					histData.append(row['PST.EXP.CLD.'])
			elif category=="Difficulty":
				if row['PST.EXP.BED.'] != "NA" and row['PST.EXP.BED.'] != "NaN":
					histData.append(row['PST.EXP.BED.'])
			elif category=="Performance":
				if row['TSK.PRB.ANS.'] != "NA" and row['TSK.PRB.ANS.'] != "NaN":
					histData.append(row['TSK.PRB.ANS.'])
			elif category=="Confidence":
				if row['TSK.CON.'] != "NA" and row['TSK.CON.'] != "NaN":
					histData.append(row['TSK.CON.'])
			elif category=="Time":
				if row['TSK.TIME.DIFF.'] != "NA" and row['TSK.TIME.DIFF.'] != "NaN" and row['TSK.TIME.DIFF.'] > 0 and row['TSK.TIME.DIFF.'] < 3000:
					histData.append(row['TSK.TIME.DIFF.'])

		return JsonResponse({"data":json.dumps(histData)})
	else:
		return JsonResponse({"request": "Not Supported"})

@login_required(login_url='/tasking/login')
def view_status(request):
	if user_authorized(request):
		experiments = Experiment.objects.all()
		masterList = {}
		for experiment in experiments:
			name = experiment.name
			userprofiles = experiment.userprofile_set.all()
			usp = sorted(userprofiles)
			products = []
			tasks = []
			tasklists = {}
			completedTasks = []
			incompleteTasks = []
			experimentList = {}
			for userprofile in userprofiles:
				tasklistitems = userprofile.tasklistitem_set.all()
				for tasklistitem in tasklistitems:
					products.append(tasklistitem.product)
					# tasklist[product][task]
					# {"A":[t1, t2, t3], "B":[t4, t5], "C":[t6]}
					tasks.append(tasklistitem.op_task)
					if not (tasklistitem.product.name in tasklists):
						tasklists[tasklistitem.product.name] = []
					if not (tasklistitem.op_task.name in tasklists[tasklistitem.product.name]):
						tasklists[tasklistitem.product.name].append(tasklistitem.op_task.name)
					if tasklistitem.task_complete is True:
						completedTasks.append(tasklistitem)
					else:
						incompleteTasks.append(tasklistitem)
			totalTasks = float(len(completedTasks) + len(incompleteTasks))
			if totalTasks != 0:
				percentageComplete = int((len(completedTasks) / totalTasks) * 100)
			else:
				percentageComplete = 0
			sortedProd = sorted(set(products))
			sortedTasks = sorted(set(tasks))
			sortedCompletedTasks = sorted(completedTasks)
			sortedIncompleteTasks = sorted(incompleteTasks)
			experimentList["users"] = usp
			experimentList["products"] = sortedProd
			experimentList["tasks"] = sortedTasks
			experimentList["tasklists"] = json.dumps(tasklists)
			#experimentList["tasklists"] = tasklists
			experimentList["completedTasks"] = sortedCompletedTasks
			experimentList["incompleteTasks"] = sortedIncompleteTasks
			experimentList["percentageComplete"] = percentageComplete
			masterList[name] = experimentList
		return render(request, 'status.html', {'experimentList': masterList})


@login_required(login_url='/tasking/login')
def manage_exps(request):
	if user_authorized(request):
		experimentlist = Experiment.objects.all()
		return render(request, 'experiments.html', {'experimentlist': experimentlist})


@login_required(login_url='/tasking/login')
def view_exp_details(request, exppk):
	if user_authorized(request):
		experiment = Experiment.objects.get(id=exppk)
		return render(request, 'experiment_details.html', {'experiment':experiment})


@login_required(login_url='/tasking/login')
def add_exp(request):
	if user_authorized(request):
		if request.method == 'POST':
			experiment = Experiment()
			experiment.name = request.POST['exp_name']
			experiment.task_count = request.POST['exp_taskcount']
			experiment.task_length = request.POST['exp_tasklength']
			experiment.has_achievements = request.POST.get('exp_achievements', False)
			experiment.has_intake = request.POST.get('exp_intake', False)
			experiment.intake_url = request.POST.get('exp_intake_url', False)
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
	if user_authorized(request):
		experiment = Experiment.objects.get(id=exppk)
		experiment.name = request.POST['exp_name']
		experiment.task_count = request.POST['exp_taskcount']
		experiment.task_length = request.POST['exp_tasklength']
		experiment.has_achievements = request.POST.get('exp_achievements', False)
		experiment.has_intake = request.POST.get('exp_intake', False)
		experiment.intake_url = request.POST.get('exp_intake_url', False)
		experiment.has_followup = request.POST.get('exp_followup', False)
		experiment.consent = request.POST.get('exp_consent', False)
		experiment.sequential_tasks = request.POST.get('exp_sequentialtasks', False)
		experiment.show_progress = request.POST.get('exp_progress', False)
		experiment.timed = request.POST.get('exp_timed', False)

		experiment.save()
		return redirect('exp_portal:manage_exps')


@login_required(login_url='/tasking/login')
def manage_datasets(request):
	if user_authorized(request):
		datasets = Dataset.objects.all()
		return render(request, 'datasets.html', {'datasets':datasets})


@login_required(login_url='/tasking/login')
def view_dataset_details(request, datasetpk):
	if user_authorized(request):
		dataset = Dataset.objects.get(id=datasetpk)
		return render(request, 'dataset_details.html', {'dataset':dataset})


@login_required(login_url='/tasking/login')
def add_dataset(request):
	if user_authorized(request):
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
	if user_authorized(request):
		dataset = Dataset.objects.get(id=datasetpk)
		dataset.name = request.POST['dataset_name']
		dataset.version = request.POST['dataset_version']
		dataset.is_active = request.POST.get('dataset_active', False)

		dataset.save()

		return redirect('exp_portal:manage_datasets')


@login_required(login_url='/tasking/login')
def view_experiment_products(request):
	if user_authorized(request):
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
