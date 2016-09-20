# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from django.shortcuts import render, redirect
from op_tasks.models import UserProfile
from django.core import mail
from django.conf import settings
from tasks import user_authorized
from xdata.settings import LOGIN_URL

from django.contrib.auth.decorators import login_required


def send_email(request):
    print request
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
    if user_authorized(request):
        return render(request, 'email_form.html', {'userprofiles': userprofiles, 'status': status, 'statusMessage': statusMessage})
    else:
        return redirect(LOGIN_URL)


def printme(string):
    print string
