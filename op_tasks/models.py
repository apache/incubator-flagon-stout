from django.db import models
from django.contrib.auth.models import User
import hashlib
import time

def _createHash():
    hash = hashlib.sha1()
    hash.update(str(time.time()))
    return hash.hexdigest()[:-10]

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

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    user_hash = models.CharField(max_length=30, default=_createHash, unique=True, editable=False)
    progress = models.IntegerField(default=0)

    # additional user parameters
    exp_inst_complete = models.BooleanField(default=False)
    portal_inst_complete = models.BooleanField(default=False)
    task_inst_complete = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username

    def read_instructions(self):
        return self.exp_inst_complete and self.portal_inst_complete and self.task_inst_complete

    # read_instructions = property(_read_instructions)

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
    exit_active = models.BooleanField(default=False)
    exit_complete = models.BooleanField(default=False)

    def _both_complete(self):
        "returns whether both task and survey are complete"
        return self.exit_complete and self.task_complete

    both_complete = property(_both_complete)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s, %s, %s' % (self.userprofile.user.username, self.op_task, self.index)

    class Meta:
        ordering = ('userprofile', 'index')
    # index = models.IntegerField()

# class Achievments(models.Model):
    