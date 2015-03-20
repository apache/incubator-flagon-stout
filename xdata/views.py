from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.template import RequestContext
from django.contrib.auth.views import login as login_view

from forms import *

def index(request):
    return render_to_response('index.html')

# def contact(request):
#     if request.method == 'POST': # If the form has been submitted...
#         # ContactForm was defined in the previous section
#         form = ExampleForm(request.POST) # A form bound to the POST data
#         if form.is_valid(): # All validation rules pass
#             # Process the data in form.cleaned_data
#             # ...
#             return HttpResponseRedirect('/op_tasks/task_list/') # Redirect after POST
#     else:
#         form = ExampleForm() # An unbound form

#     return render(request, 'question.html', {
#         'form': form,
#     })