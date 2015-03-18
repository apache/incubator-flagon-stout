from django.contrib import admin
from op_tasks.models import Product, Dataset, TaskListItem, UserProfile, OpTask

adminsite = admin.site

class DatasetAdmin(admin.ModelAdmin):
	search_fields = ['name', 'is_active']
	list_display = ['name', 'version', 'is_active']

class UserProfileAdmin(admin.ModelAdmin):
	search_fields = ['user', 'progress']
	list_display = ['user', 'progress', 'exp_inst_complete', 'portal_inst_complete', 'task_inst_complete']

# Defines how the products are viewed
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'team', 'dataset', 'is_active']
    list_display = ['team', 'name', 'version', 'dataset', 'url', 'instructions']

# Defines how the operational tasks are viewed
class OpTaskAdmin(admin.ModelAdmin):
	search_fields = ['name', 'is_active', 'dataset']
	list_display = ['name', 'is_active', 'dataset', 'survey_url', 'instructions', 'exit_url']

# Defines how the task list items are viewed
class TaskListItemAdmin(admin.ModelAdmin):
	search_fields = ['user__email']	
	list_display = ['userprofile', 'op_task', 'index', 'task_active', 'task_complete', 'exit_complete']

adminsite.register(OpTask, OpTaskAdmin)
adminsite.register(Product, ProductAdmin)
adminsite.register(TaskListItem, TaskListItemAdmin)
adminsite.register(Dataset, DatasetAdmin)
adminsite.register(UserProfile, UserProfileAdmin)