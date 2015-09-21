from django.shortcuts import render
from op_tasks.models import Experiment
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import os

from models import Document
from forms import DocumentForm

def list(request):
    # Handle file uploads
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES, request.POST.get('dirName', 'error'))

        # redirect to the document after POST
        return HttpResponseRedirect(reverse('uploads.views.list'))

    else:
        form = DocumentForm() # An empty, unbound form
        experiments = Experiment.objects.all()
        # Render list page with the documents and the form
        return render(request, 'list.html', {'form': form, 'experiments': experiments})

def handle_uploaded_file(f, dirname):
    path = os.path.join('../', dirname)
    try:
        os.mkdir(path)
    except:
        pass
    file = f['docfile']
    with open(path  + '/' + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)