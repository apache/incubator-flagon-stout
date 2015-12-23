from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
#from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from elasticsearch import Elasticsearch
from xdata.settings import ALE_URL
from axes.decorators import watch_login
import achievements
import tasksUtil
import exp_portal
import datetime

import exceptions
import hashlib
import logging
#import zlib
#import sqlite

from op_tasks.models import Dataset, Product, OpTask, UserProfile, TaskListItem, Experiment

logger = logging.getLogger('op_tasks')

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

# connects with User-ALE to count activities.  
def count_activities(session_id):
    XDATA_INDEX="xdata_v3"

    es = Elasticsearch(ALE_URL)

    queryData = {}
    fieldFilter = ["timestamp", "sessionID", "parms.desc"]

    queryData["query"] = { "match": { "sessionID" : session_id } }
    results = es.search(index=XDATA_INDEX, body=queryData, fields=fieldFilter, size=1000)['hits']
    timestamps = [d['fields']['timestamp'] for d in results['hits']]
    return len(timestamps)
   
# manages which prodct is delivered to the current user
@login_required(login_url='/tasking/login')
def product(request, task_pk):
    if request.method == 'POST':
        user = request.user
        userprofile = user.userprofile

        print 'Task primary key: ', task_pk, ' completed'
        try:
            # get current sequence from user, this ensures that current user
            # can only get sequences assigned to him/her
            current_tasklistitem = userprofile.tasklistitem_set.get(pk=task_pk)
        except:
            return HttpResponseRedirect("/tasking/task_list")

        tasklist_length = len(userprofile.tasklistitem_set.all())
        
        if userprofile.experiment.sequential_tasks == True:

            # if it's not the last task, make the next task active
            if current_tasklistitem.index < (tasklist_length - 1):
                next_tasklistitem = userprofile.tasklistitem_set.get(index=current_tasklistitem.index+1)
            
            # if you got here because you just completed a task,
            # then set it complete and make the exit task active
            if current_tasklistitem.task_complete == False:
                current_tasklistitem.task_complete = True
                current_tasklistitem.task_active = False
                current_tasklistitem.exit_active = True
                current_tasklistitem.date_complete = timezone.localtime(timezone.now())
                sessionID = '%s::%s' % (userprofile.user_hash, current_tasklistitem.pk)
                try:
                    current_tasklistitem.activity_count = 0
                    # current_tasklistitem.activity_count = count_activities(sessionID)
                except Exception as inst:
                    # print inst
                    current_tasklistitem.activity_count = 0
                userprofile.progress += 20
                print 'task complete', timezone.now()
            
            # you likely got here because you just completed an exit task
            # so mark it complete and move 
            else:
                current_tasklistitem.exit_active = False
                current_tasklistitem.exit_complete = True
                print 'survey complete', current_tasklistitem.index
                userprofile.progress += 15
                if current_tasklistitem.index < tasklist_length - 1:
                    next_tasklistitem.task_active = True
                    next_tasklistitem.save()
                else:
                    current_tasklistitem.save()

        elif userprofile.experiment.sequential_tasks == False:
            print "no sequencing"

            if current_tasklistitem.task_complete == False:
                current_tasklistitem.task_complete = True
                current_tasklistitem.exit_active = True
                current_tasklistitem.date_complete = timezone.localtime(timezone.now())
                print timezone.localtime(timezone.now())

            else:
                current_tasklistitem.exit_active = False
                current_tasklistitem.exit_complete = True

        userprofile.save()
        current_tasklistitem.save()
        return HttpResponseRedirect("/tasking/task_list")

    # if method is GET just show the product page
    user = request.user
    userprofile = user.userprofile
    tasklistitem = TaskListItem.objects.get(pk=task_pk)
    current_task = tasklistitem.op_task
    request.session['current_optask'] = current_task.pk

    response = render(request, 'product.html', {
    	'product': tasklistitem.product,
        'task_pk': task_pk,
        'product_url': tasklistitem.product.url + ('?USID=%s::%s' % (userprofile.user_hash, tasklistitem.pk)),
    	'op_task': current_task
    	})
    set_cookie(response, 'USID', '%s::%s' % (userprofile.user_hash, tasklistitem.pk))
    return response


def product_test(request, task_pk):
    user = request.user
    userprofile = user.userprofile
    tasklistitem = TaskListItem.objects.get(pk=task_pk)
    current_task = tasklistitem.op_task
    request.session['current_optask'] = current_task.pk

    response = redirect(tasklistitem.product.url + ('?USID=%s::%s' % (userprofile.user_hash, tasklistitem.pk) ) )
    set_cookie(response, 'USID', '%s::%s' % (userprofile.user_hash, tasklistitem.pk))
    return response


def task_test(request, task_pk):
    user = request.user
    userprofile = user.userprofile
    tasklistitem = TaskListItem.objects.get(pk=task_pk)
    current_task = tasklistitem.op_task
    request.session['current_optask'] = current_task.pk
    userAleUrl = settings.ALE_URL 

    return render(request, 'task.html', {'tasklistitem':tasklistitem, 'userAleUrl': userAleUrl})


def task_launch(request, task_pk):
    tasklistitem = TaskListItem.objects.get(pk=task_pk)
    userAleUrl = settings.ALE_URL 

    return render(request, 'task_launch.html', {'tasklistitem': tasklistitem, 'userAleUrl': userAleUrl})

# creates a new user and assigns tasks 
def register(request):
    # TODO : add logging back in.  Good practice!!
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registrationSuccessful = False
    userExists = False
    error = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':

        # Now we hash the password with the set_password method.
        # Once hashed, we can update the user object.
        user = get_user_model()(email=request.POST['email'])
        user.set_password(request.POST['password'])
        user.last_login = '1970-01-01 00:00'
        
        if not user.email or not request.POST['password']:
            error = True
            return render_to_response('registration/register.html', {'registrationSuccessful': registrationSuccessful, 'userExists': userExists, 'error': error}, context)
        
        try:
            user.save()
        except IntegrityError:
            userExists = True
            return render_to_response('registration/register.html', {'registrationSuccessful': registrationSuccessful, 'userExists': userExists, 'error': error}, context)

        # Now sort out the UserProfile instance.
        # Since we need to set the user attribute ourselves, we set commit=False.
        # This delays saving the model until we're ready to avoid integrity problems.
        userprofile = UserProfile()
        userprofile.user = user

        # TODO: change this from default experiment 
        saved_experiments = Experiment.objects.get(name='2015_public_xdataonline')
        userprofile.experiment = Experiment.objects.get(name='2015_public_xdataonline')

        # Now we save the UserProfile model instance.
        userprofile.save()

        # Finally we assign tasks to the new user
        # Get a random product, get a random order of tasks
        # And save them to the task list
        product = Product.objects.filter(is_active=True).order_by('?')[0]
        dataset = product.dataset
        tasks = dataset.optask_set.filter(is_active=True).order_by('?')

        for index, task in enumerate(tasks):
            TaskListItem(userprofile=userprofile, op_task=task, product=product, 
                index=index, task_active=False).save()


        # Update our variable to tell the template registration was successful.
        registrationSuccessful = True

        # add some logic to log events, log in users directly
        print "successful registration of " + request.POST['email'] +" "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request.POST['email_to'] = user.email
        request.POST['email_subject'] = 'Welcome to XDATA Online'
        request.POST['email_message'] = 'Your registration was successful!\n\nIn case you forget your password, please go to the following page and reset your password:\n\nhttps://' + get_current_site(request).domain + '/tasking/reset/\n\nYour username, in case you\'ve forgotten, is the email address this message was sent to.\n\nThanks for using our site!\n\nThe ' + get_current_site(request).name + ' team' 
        exp_portal.email.send_email(request)

        # login_participant(request)
        # return render(request, 'instructions/exp_instructions.html', {'user': request.user})

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    # else:
        # print "register without POST"
        # not sure what code belongs here yet but the two lines below are legacy...
        # user_form = UserForm()
        # profile_form = UserProfileForm()

    # Render the template depending on the context.
    # possibly change this to render task list - see notes above
    return render_to_response('registration/register.html', {'registrationSuccessful': registrationSuccessful, 'userExists': userExists, 'error': error}, context)


def logout_participant(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')


@watch_login
def login_participant(request):
	# Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username (email) and password provided by the user.
        # This information is obtained from the login form.
        email = request.POST['email']
        password = request.POST['password']
        # print "Login attempt by " + username + " at " + datetime

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
                return HttpResponseRedirect('/tasking/task_list')
                # return render(request, 'task_list.html', {'user': user})
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
        # experiment_title = title
        return render(request, 'registration/login.html')
        # return render(request, 'registration/login.html', {'experiment_title': experiment_title})


	# return login_view(request, authentication_form=MyAuthForm)


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='registration/reset_password_confirm.html',
                                  uidb64=uidb64, token=token,
                                  post_reset_redirect=reverse('op_tasks:login'))


def reset(request):
    return password_reset(request, template_name='registration/reset_password_form.html',
                          email_template_name='registration/reset_password_email.html',
                          post_reset_redirect=reverse('op_tasks:reset_sent'),
                          from_email=settings.EMAIL_FROM_NOMINAL_ADDRESS)


def reset_sent(request):
    return render(request, 'registration/reset_password_done.html')


@login_required(login_url='/tasking/login')
def task_list(request):
    # print [x.both_complete for x in userprofile.tasklistitem_set.all()]
    user = request.user
    userprofile = user.userprofile
    all_complete = all([x.both_complete for x in userprofile.tasklistitem_set.all()])
    # handling for instructions & intake, transition to first OpTask when ready
    if userprofile.tasklistitem_set.all().count() > 0:
        first_task = userprofile.tasklistitem_set.all()[0]
        if userprofile.exp_inst_complete and userprofile.portal_inst_complete and not first_task.task_complete:
            if userprofile.experiment.has_intake:
                if userprofile.intake_complete:
                    first_task.task_active = True
                    first_task.save()
            else:
                if userprofile.experiment.sequential_tasks:
                    first_task.task_active = True
                    first_task.save()
                else:
                    for task in userprofile.tasklistitem_set.all():
                        task.task_active = True
                        task.save()
    
    # On visiting the task_list page, run check achievements logic
    # TODO this isn't scalable... need a better strategy here
    achievements.checkAchievements(request)
    
    return render(request, 'task_list.html', 
        {'userprofile': userprofile, 'all_complete': all_complete,
         'hasTasksCompleteOneAchievement': achievements.hasTasksCompleteOneAchievement(user),
         'hasTasksCompleteTwoAchievement': achievements.hasTasksCompleteTwoAchievement(user),
         'hasFreePlayAchievement': achievements.hasFreePlayAchievement(user)})
    

def activate_free_play(request):
    """
    In "Free Play" mode, the user has access to all of the tasks in the system
    for the products they are applicable to. The "buffet" style of tasking.
    """
    user = request.user
    userprofile = user.userprofile
    
    """
    First, award the Free Play achievement, if the user doesn't already have it.
    """
    achievements.awardFreePlayAchievement(user)
    
    """
    Then append the buffet of taskings to the user's task list.
    """
    tasksUtil.appendAllTasks(user)
    
    # Then follow the same logic as displaying the task_list page
    return task_list(request)


def intro(request, process=None):
    if process == 'register':
        next_page = '/tasking/register'
    elif process == 'login':
        next_page = '/tasking/login'
    return render(request, 'intro.html', {'user': request.user, 'next_page': next_page})


def safety(request):
    return redirect('http://www.xdataonline.com')


def instruct(request, read=None):
    user = request.user
    userprofile = user.userprofile

    if read == 'experiment':
        if not userprofile.exp_inst_complete:
            userprofile.exp_inst_complete = True
            userprofile.progress += 15

    elif read == 'portal':
        if not userprofile.portal_inst_complete:
            userprofile.portal_inst_complete = True
            userprofile.progress += 15

    elif read == 'product':
        if not userprofile.task_inst_complete:
            user.userprofile.task_inst_complete = True
            userprofile.progress += 10

    userprofile.save()
    product = userprofile.tasklistitem_set.all()[0].product
    
    return render(request, 'instruction_home.html',
                  {'user': request.user, 'product': product,
                   'hasTasksCompleteOneAchievement': achievements.hasTasksCompleteOneAchievement(user),
                   'hasTasksCompleteTwoAchievement': achievements.hasTasksCompleteTwoAchievement(user),
                   'hasFreePlayAchievement': achievements.hasFreePlayAchievement(user)})


def intake(request):
    # TODO: not great, but a simple solution for now... we will
    # instantly mark the intake questionnaire as complete on view of the page
    user = request.user
    userprofile = user.userprofile
    userprofile.intake_complete = True
    userprofile.save()
    return render(request, 'intake.html', {'user': request.user})


def exp_instruct(request):
    user = request.user
    return render(request, 'instructions/exp_instructions.html', 
                  {'user': request.user,
                   'hasTasksCompleteOneAchievement': achievements.hasTasksCompleteOneAchievement(user),
                   'hasTasksCompleteTwoAchievement': achievements.hasTasksCompleteTwoAchievement(user),
                   'hasFreePlayAchievement': achievements.hasFreePlayAchievement(user)})


def portal_instruct(request):
    user = request.user
    return render(request, 'instructions/portal_instructions.html', 
                  {'user': request.user,
                   'hasTasksCompleteOneAchievement': achievements.hasTasksCompleteOneAchievement(user),
                   'hasTasksCompleteTwoAchievement': achievements.hasTasksCompleteTwoAchievement(user),
                   'hasFreePlayAchievement': achievements.hasFreePlayAchievement(user)})


def product_instruct(request):
    user = request.user
    return render(request, 'instructions/product_instructions.html', 
                  {'user': request.user,
                   'hasTasksCompleteOneAchievement': achievements.hasTasksCompleteOneAchievement(user),
                   'hasTasksCompleteTwoAchievement': achievements.hasTasksCompleteTwoAchievement(user),
                   'hasFreePlayAchievement': achievements.hasFreePlayAchievement(user)})


def view_profile(request):
    user = request.user
    return render(request, 'user_profile.html',
                  {'user': request.user,
                   'hasTasksCompleteOneAchievement': achievements.hasTasksCompleteOneAchievement(user),
                   'hasTasksCompleteTwoAchievement': achievements.hasTasksCompleteTwoAchievement(user),
                   'hasFreePlayAchievement': achievements.hasFreePlayAchievement(user)})
