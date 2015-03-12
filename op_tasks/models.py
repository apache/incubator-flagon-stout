from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import time
import hashlib

# the dataset class stores parameters about the 
class Dataset(models.Model):
    name = models.CharField(max_length=1000) # name of dataset
    version = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s - %s' % (self.name, self.version)
    class Meta:
        unique_together = ("name", "version")

class Product(models.Model): # product = tool + dataset
    dataset = models.ForeignKey(Dataset, null=True, blank=True) # data for tool
    url = models.CharField(max_length=1000, unique=True) # path to product 
    team = models.CharField(max_length=1000) # developer team
    name = models.CharField(max_length=1000) # name of 
    version = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    instructions = models.CharField(max_length=1000) 
    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s:%s:%s:%s' % (self.team, self.name, self.dataset, self.version)

class OpTask(models.Model):
    dataset = models.ForeignKey(Dataset, null=True, blank=True)
    name = models.CharField(max_length=200)
    survey_url = models.CharField(max_length=1000, unique=False)
    is_active = models.BooleanField(default=True)
    exit_url = models.CharField(max_length=1000, unique=False)
    instructions = models.CharField(max_length=1000)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s-%s' % (self.name, self.dataset)


# This function generate 10 character long hash
def _createHash():
    hash = hashlib.sha1()
    hash.update(str(time.time()))
    return  hash.hexdigest()[:-10]

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    # additional user parameters
    exp_inst_complete = models.BooleanField(default=False)
    portal_inst_complete = models.BooleanField(default=False)
    task_inst_complete = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username
## old User models BEGIN
# Creates and saves a User with the given username, email and password.
# class ParticipantManager(BaseUserManager):
#     def _create_user(self, username, email, password,
#                      is_staff, is_superuser, **extra_fields):
#         now = timezone.now()
#         if not username:
#             raise ValueError('The given username must be set')
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email,
#                           is_staff=is_staff, is_active=True,
#                           is_superuser=is_superuser, last_login=now,
#                           date_joined=now, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, username, email=None, password=None, **extra_fields):
#         return self._create_user(username, email, password, False, False,
#                                  **extra_fields)

#     def create_superuser(self, username, email, password, **extra_fields):
#         return self._create_user(username, email, password, True, True,
#                                  **extra_fields)

# # Change models so participant has a sequence and not the other way around
# class Participant(AbstractBaseUser):
#     op_tasks = models.ManyToManyField(OpTask, through='TaskListItem', blank=True)
#     product = models.ForeignKey(Product)
#     user_hash = models.CharField(
#         max_length=30, 
#         default=_createHash,
#         unique=True,
#         editable=False)
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     is_staff = False
#     date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

#     objects = ParticipantManager()

#     USERNAME_FIELD = 'email'    

#     # Returns the first_name plus the last_name, with a space in between.
#     def get_full_name(self):
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()

#     def get_short_name(self):
#         "Returns the short name for the user."
#         return self.first_name

#     # sends an email to this user
#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """
#         Sends an email to this User.
#         """
#         send_mail(subject, message, from_email, [self.email], **kwargs)
## Old User models END


# The TaskListItem model is used to manage user navigation through the experiment
class TaskListItem(models.Model):
    # knows which user it is assigned to
    user = models.ForeignKey(UserProfile)
    # knows which operational task  
    op_task = models.ForeignKey(OpTask)
    # is assigned an index in a list
    index = models.IntegerField()
    # mark if operation task is completed
    ot_complete = models.BooleanField(default=False)
    # mark if this operational task is the current task in the sequence
    ot_active = models.BooleanField(default=False)
    exit_active = models.BooleanField(default=False)
    exit_complete = models.BooleanField(default=False)

    def _both_complete(self):
        "returns whether both task and survey are complete"
        return self.exit_complete and self.ot_complete

    both_complete = property(_both_complete)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s, %s, %s' % (self.user, self.op_task, self.index)

    class Meta:
        ordering = ('user', 'index')
    # index = models.IntegerField()

# WHAT IS THIS CLASS FOR?
class MyBackend(object):
    def authenticate(self, email=None, password=None, **kwargs):
        print 'authenticate', email
        # UserModel = get_user_model()
        if email is None:
            email = kwargs.get(Participant.USERNAME_FIELD)
        try:
            participant = Participant._default_manager.get_by_natural_key(email)
            if participant.check_password(password):
                return participant
        except Participant.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            Participant().set_password(password)
    def get_user(self, user_id):
        # UserModel = get_user_model()
        try:
            return Participant._default_manager.get(pk=user_id)
        except Participant.DoesNotExist:
            return None