from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login as login_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.template import RequestContext
from django.conf import settings

import datetime
from op_tasks.models import *
from op_tasks.forms import *

@login_required
def index(request):
	# return HttpResponse("hello, you're at the index")

	op_task = OpTask.objects.get(pk=1)	

	return render(request, 'question.html', {
	    'op_task': op_task
	})

import datetime

def set_cookie(response, key, value, days_expire = 7):
  if days_expire is None:
    max_age = 365 * 24 * 60 * 60  #one year
  else:
    max_age = days_expire * 24 * 60 * 60 
  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, 
  	max_age=max_age, 
  	expires=expires, 
  	domain=settings.SESSION_COOKIE_DOMAIN, 
  	secure=None)

##########################################
#
# product method to capture redirects from 
# completion of OT's
#
#########################################    
def product(request, seq_pk):
    if request.method == 'POST':
        user = request.user

        print 'SEQPK', seq_pk
        try:
            # get current sequence from user, this ensures that current user
            # can only get sequences assigned to him/her
            current_sequence = user.sequence_set.get(pk=seq_pk)
        except:
            return HttpResponseRedirect("/op_tasks/task_list")

        seq_length = len(user.sequence_set.all())
        
        # if it's not the last task, make the next task active
        if current_sequence.index < (seq_length - 1):
            next_sequence = user.sequence_set.get(index=current_sequence.index+1)
        
        # if you got here because you just completed a task,
        # then set it complete and make the exit task active
        if current_sequence.ot_complete == False:
            current_sequence.ot_complete = True
            current_sequence.ot_active = False
            current_sequence.exit_active = True
        
        # you likely got here because you just completed an exit task
        # so mark it complete and move 
        else:
            current_sequence.exit_active = False
            current_sequence.exit_complete = True
            print 'survey complete', current_sequence.index
            if current_sequence.index < 1:
                next_sequence.ot_active = True
                next_sequence.save()
            else:
                current_sequence.save()
        current_sequence.save()
        return HttpResponseRedirect("/op_tasks/task_list")

    # if method is GET just show the product page
    user = request.user
    seq = Sequence.objects.get(pk=seq_pk)
    cur_task = seq.op_task
    request.session['current_optask'] = cur_task.pk



    response = render(request, 'product.html', {
    	'product': user.product,
        'seq_pk': seq_pk,
        'product_url': user.product.url + ('?USID=%s::%s' % (user.user_hash, seq.pk)),
    	'op_task': cur_task
    	})
    set_cookie(response, 'USID', '%s::%s' % (user.user_hash, seq.pk))
    return response


####################################################
#
#
#
####################################################
def register(request):
    # if POST method then submit information
    if request.method == 'POST':
        form = ParticipantCreationForm(request.POST)
        if form.is_valid():
        	# write the new user to the db
            new_user = form.save()	
            new_user.backend = 'op_tasks.models.MyBackend'
            login(request, new_user)

            # and redirect to the task list
            return HttpResponseRedirect("/op_tasks/task_list")
    # if GET method then just load the page
    else: 
        form = ParticipantCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })    

def logout_participant(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

def login_participant(request):
	# Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        email = request.POST['email']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(email=email, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/op_tasks/task_list')
                # return render(request, 'task_list.html', {'user': request.user})
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your XDATA account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(email, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('registration/login.html', {}, context)

	# return login_view(request, authentication_form=MyAuthForm)

@login_required(login_url='/op_tasks/login')
def task_list(request):
    # print [x.both_complete for x in user.sequence_set.all()]
    user = request.user
    all_complete = all([x.both_complete for x in user.sequence_set.all()])
    return render(request, 'task_list.html', 
        {'user': user, 'all_complete': all_complete}
        )

def intro(request):
    return render(request, 'intro.html', {'user': request.user})

def login_intro(request):
    return render(request, 'login_intro.html', {'user': request.user})

def instruct(request):
    return render(request, 'instruction_home.html', {'user': request.user})










