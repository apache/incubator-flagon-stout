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
def product(request, task_pk):
    if request.method == 'POST':
        user = request.user

        print 'Task primary key:', task_pk
        try:
            # get current sequence from user, this ensures that current user
            # can only get sequences assigned to him/her
            current_sequence = user.tasklistitem_set.get(pk=task_pk)
        except:
            return HttpResponseRedirect("/op_tasks/task_list")

        seq_length = len(user.tasklistitem_set.all())
        
        # if it's not the last task, make the next task active
        if current_sequence.index < (seq_length - 1):
            next_sequence = user.tasklistitem_set.get(index=current_sequence.index+1)
        
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
    task = TaskListItem.objects.get(pk=task_pk)
    cur_task = task.op_task
    request.session['current_optask'] = cur_task.pk

    response = render(request, 'product.html', {
    	'product': user.product,
        'task_pk': task_pk,
        'product_url': user.product.url + ('?USID=%s::%s' % (user.user_hash, task.pk)),
    	'op_task': cur_task
    	})
    set_cookie(response, 'USID', '%s::%s' % (user.user_hash, task.pk))
    return response

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        print "POST"
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        # profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid(): # and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = UserProfile.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True
            print "successful registration"
            return HttpResponseRedirect("/op_tasks/task_list")

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors#, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        #profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'registration/register.html',
            {'user_form': user_form, 'registered': registered},
            context)

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
    # print [x.both_complete for x in user.tasklistitem_set.all()]
    user = request.user
    all_complete = all([x.both_complete for x in user.tasklistitem_set.all()])
    return render(request, 'task_list.html', 
        {'user': user, 'all_complete': all_complete}
        )

def intro(request):
    return render(request, 'intro.html', {'user': request.user})

def login_intro(request):
    return render(request, 'login_intro.html', {'user': request.user})

def instruct(request):
    return render(request, 'instruction_home.html', {'user': request.user})

def exp_instruct(request):
    return render(request, 'exp_instructions.html', {'user': request.user})

def task_instruct(request):
    return render(request, 'task_instructions.html', {'user': request.user})


