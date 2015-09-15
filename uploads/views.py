from django.shortcuts import render_to_response
from op_tasks.models import Experiment
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import Document
from forms import DocumentForm

def list(request):
    # Handle file uploads
    if request.method == 'POST':
        # form = DocumentForm(request.POST, request.FILES)
        # if form.is_valid():
        newdoc = Document(docfile = request.FILES['docfile'])
        newdoc.save()

        # redirect to the document after POST
        return HttpResponseRedirect(reverse('uploads.views.list'))

    else:
        form = DocumentForm() # An empty, unbound form

    experiments = Experiment.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'form': form, 'experiments': experiments},
        context_instance=RequestContext(request)
    )
