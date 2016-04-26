from django.shortcuts import render, redirect
from op_tasks.models import UserProfile
from django.core import mail
from django.conf import settings
from tasks import user_authorized
from base import LOGIN_URL

from django.contrib.auth.decorators import login_required


def send_email(request):
    print request
    if request.method == 'POST':
        email_to = request.POST.get('email_to', settings.EMAIL_TO_ERROR_ADDRESS)
        subject = request.POST.get('email_subject', 'error')
        message = request.POST.get('email_message', 'error')
        print email_to, subject, message
        status = mail.send_mail(subject, message, settings.EMAIL_FROM_NOMINAL_ADDRESS, [email_to], fail_silently=False)
    else:
        status = 2

    userprofiles = UserProfile.objects.all()
    if status == 0:
        statusMessage = "The email did not send. Try again."
    elif status == 1:
        statusMessage = "Email sent!"
    elif status == 2:
        statusMessage = ""
    if user_authorized(request):
        return render(request, 'email_form.html', {'userprofiles': userprofiles, 'status': status, 'statusMessage': statusMessage})
    else:
        return redirect(LOGIN_URL)


def printme(string):
    print string
