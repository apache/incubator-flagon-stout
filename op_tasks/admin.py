from django.contrib import admin
from op_tasks.models import Product, Dataset, TaskListItem, UserProfile, OpTask

adminsite = admin.site

# Defines how the products are viewed
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'team']
    list_display = ['team', 'name', 'version']

# Defines how the operational tasks are viewed
class OpTaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'dataset', 'survey_url', 'exit_url']

# Defines how the task list items are viewed
class TaskListItemAdmin(admin.ModelAdmin):
	search_fields = ['user__email']	
	list_display = ['userprofile', 'op_task', 'index', 'task_complete', 'exit_complete']

adminsite.register(OpTask, OpTaskAdmin)
adminsite.register(Product, ProductAdmin)
adminsite.register(TaskListItem, TaskListItemAdmin)
adminsite.register(Dataset)
adminsite.register(UserProfile)