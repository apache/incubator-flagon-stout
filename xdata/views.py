from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.template import RequestContext
from django.contrib.auth.views import login as login_view

from forms import *

def index(request):
    return render(request, 'index.html')

def user_feedback_home(request):
	return render(request, 'user_feedback_index.html')
