from django.shortcuts import render, redirect
from op_tasks.models import UserProfile, Product, Dataset, OpTask, TaskListItem, Experiment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def view_tasks(request):
	tasks = OpTask.objects.all()
	datasets = Dataset.objects.all()
	return render(request, 'tasks.html', {'tasks': tasks, 'datasets':datasets})

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

def delete_task(request, taskpk):
	task = OpTask.objects.get(id=taskpk)
	task.delete()

	return redirect('exp_portal:view_tasks')
