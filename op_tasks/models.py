from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
import hashlib
import time, datetime


def _createHash():
    hash = hashlib.sha1()
    hash.update(str(time.time()))
    return hash.hexdigest()[:-10]


# the dataset class stores parameters about the 
class Dataset(models.Model):
    name = models.CharField(max_length=255) # name of dataset
    version = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s - %s' % (self.name, self.version)

    class Meta:
        unique_together = ("name", "version")


class Product(models.Model): # product = tool + dataset
    dataset = models.ForeignKey(Dataset, null=True, blank=True) # data for tool
    url = models.CharField(max_length=255, unique=False) # path to product 
    #url = models.CharField(max_length=255, unique=False) # path to product 
    team = models.CharField(max_length=255) # developer team
    name = models.CharField(max_length=255) # name of 
    version = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    instructions = models.CharField(max_length=255)
    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s:%s:%s:%s' % (self.team, self.name, self.dataset, self.version)


class OpTask(models.Model):
    dataset = models.ForeignKey(Dataset, null=True, blank=True)
    name = models.CharField(max_length=200)
    survey_url = models.CharField(max_length=255, unique=False)
    is_active = models.BooleanField(default=True)
    exit_url = models.CharField(max_length=255, unique=False)
    instructions = models.CharField(max_length=255)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s-%s' % (self.name, self.dataset)


class Experiment(models.Model):
    name = models.CharField(max_length=250)  # name of the experiment
    task_count = models.IntegerField(default=0)  
    task_length = models.IntegerField(default=30)  # minutes
    has_achievements = models.BooleanField(default=False)
    has_intake = models.BooleanField(default=False)
    intake_url = models.CharField(max_length=255, unique=False, blank=True, default='')
    has_followup = models.BooleanField(default=False)
    consent = models.BooleanField(default=True)
    sequential_tasks = models.BooleanField(default=True)
    show_progress = models.BooleanField(default=True)
    timed = models.BooleanField(default=True)

    # auto tasking with user registration.  If FALSE then tasks must be 
    # assigned manually by admin
    auto_tasking = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' % (self.name)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    user_hash = models.CharField(max_length=30, default=_createHash, unique=True, editable=False)
    progress = models.IntegerField(default=0)

    # additional user parameters
    exp_inst_complete = models.BooleanField(default=False)
    portal_inst_complete = models.BooleanField(default=False)
    task_inst_complete = models.BooleanField(default=False)
    intake_complete = models.BooleanField(default=False)
    
    experiment = models.ForeignKey(Experiment, null=True, blank=True)
    referrals = models.IntegerField(default=0)
    bestGenAccuracy = models.IntegerField(default=0)
    bestDevAccuracy = models.IntegerField(default=0)


    def __unicode__(self):
        return self.user.email

    def read_instructions(self):
        return self.exp_inst_complete and self.portal_inst_complete and self.task_inst_complete


# The TaskListItem model is used to manage user navigation through the experiment
class TaskListItem(models.Model):
    # knows which user it is assigned to
    userprofile = models.ForeignKey(UserProfile)
    # knows which operational task  
    op_task = models.ForeignKey(OpTask)
    product = models.ForeignKey(Product)
    # is assigned an index in a list
    index = models.IntegerField()
    # mark if this operational task is the current task in the sequence
    task_active = models.BooleanField(default=False)
    # mark if operation task is completed
    task_complete = models.BooleanField(default=False)
    date_complete = models.DateTimeField(default=None, blank=True, null=True)
    exit_active = models.BooleanField(default=False)
    exit_complete = models.BooleanField(default=False)
    activity_count = models.IntegerField(default=0)

    def _both_complete(self):
        "returns whether both task and survey are complete"
        return self.exit_complete and self.task_complete

    both_complete = property(_both_complete)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s, %s, %s' % (self.userprofile.user.email, self.op_task, self.index)

    class Meta:
        ordering = ('userprofile', 'index')
    # index = models.IntegerField()


class Achievement(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=1000)

    def __unicode__(self):
        return '%s' % (self.name)


class UserAchievement(models.Model):
    userprofile = models.ForeignKey(UserProfile)
    achievement = models.ForeignKey(Achievement)

    def __unicode__(self):
        return '%s - %s' % (self.userprofile.user.email, self.achievement.name)
