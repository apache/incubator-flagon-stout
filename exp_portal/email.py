from django.shortcuts import render
from op_tasks.models import UserProfile
from django.core import mail
from django.conf import settings


def send_email(request):
    if request.method == 'POST':
        email_to = request.POST.get('email_to', 'xdataonlineerrors@gmail.com')
        subject = request.POST.get('email_subject', 'error')
        message = request.POST.get('email_message', 'error')
        print email_to, subject, message
        status = mail.send_mail(subject, message, settings.EMAIL_HOST_USER, [email_to], fail_silently=False)
    else:
        status = 2
    userprofiles = UserProfile.objects.all()
    if status == 0:
        statusMessage = "The email did not send. Try again."
    elif status == 1:
        statusMessage = "Email sent!"
    elif status == 2:
        statusMessage = ""
    return render(request, 'email_form.html', {'userprofiles': userprofiles, 'status': status, 'statusMessage': statusMessage})


def printme(string):
    print string