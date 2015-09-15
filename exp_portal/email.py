from django.shortcuts import render
from op_tasks.models import UserProfile
from django.core.mail import send_mail
from django.conf import settings


def send_email(request):
    if request.method == 'POST':
        email_to = request.POST['email-to']
        subject = request.POST['email-subject']
        message = request.POST['email-message']
        status = send_mail(subject, message, settings.EMAIL_HOST_USER, [email_to], fail_silently=True)
    else:
        status = 0
    userprofiles = UserProfile.objects.all()
    return render(request, 'email_form.html', {'userprofiles': userprofiles, 'status': status})


def email_form(request):
    userprofiles = UserProfile.objects.all()
    status = 0
    return render(request, 'email_form.html', {'userprofiles': userprofiles, 'status': status})
