from django.contrib import admin
from op_tasks.models import Product, Dataset, TaskListItem, UserProfile, OpTask, Experiment, Achievement, UserAchievement
adminsite = admin.site

class DatasetAdmin(admin.ModelAdmin):
	search_fields = ['name', 'is_active']
	list_display = ['name', 'version', 'is_active']

class UserProfileAdmin(admin.ModelAdmin):
	search_fields = ['user', 'progress']
	list_display = ['user', 'user_hash', 'experiment', 'progress', 
	'exp_inst_complete', 'portal_inst_complete', 'task_inst_complete', 'intake_complete']

# Defines how the products are viewed
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'team', 'dataset', 'is_active']
    list_display = ['team', 'name', 'version', 'dataset', 
    'url', 'instructions']

# Defines how the operational tasks are viewed
class OpTaskAdmin(admin.ModelAdmin):
	search_fields = ['name', 'is_active', 'dataset']
	list_display = ['name', 'is_active', 'dataset', 'survey_url', 
	'instructions', 'exit_url']

# Defines how the task list items are viewed
class TaskListItemAdmin(admin.ModelAdmin):
	search_fields = ['user__email']	
	list_display = ['userprofile', 'op_task', 'index', 'task_active', 
	'task_complete', 'exit_complete']

class ExperimentAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name', 'task_count', 'task_length', 
	'has_achievements', 'has_intake', 'has_followup', 'auto_tasking']
	
class AchievementAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name', 'desc']
	
class UserAchievementAdmin(admin.ModelAdmin):
	search_fields = ['userprofile']
	list_display = ['userprofile', 'achievement']

adminsite.register(OpTask, OpTaskAdmin)
adminsite.register(Product, ProductAdmin)
adminsite.register(TaskListItem, TaskListItemAdmin)
adminsite.register(Dataset, DatasetAdmin)
adminsite.register(UserProfile, UserProfileAdmin)
adminsite.register(Experiment, ExperimentAdmin)
adminsite.register(Achievement, AchievementAdmin)
adminsite.register(UserAchievement, UserAchievementAdmin)