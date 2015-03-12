from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms import ModelForm, PasswordInput, CharField
from models import *
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
    AdminPasswordChangeForm)
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.conf.urls import url
from django.contrib.admin.options import IS_POPUP_VAR

from op_tasks.forms import ParticipantCreationForm, ParticipantChangeForm
csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())

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
	list_display = ['user', 'op_task', 'index', 'ot_complete', 'exit_complete']


class ParticipantAdmin(admin.ModelAdmin):
	add_form_template = 'admin/auth/user/add_form.html'
	change_user_password_template = None
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Info', {'fields': ('user_hash',)}),		       
		('Important dates', {'fields': ('last_login', 'date_joined')}),
		('Product', {'fields': ('product',)}),
		# ('Operational Tasks' {'fields': (op_tasks_set.all())})
	)
	add_fieldsets = (
	    (None, {
	        'classes': ('wide',),
	        'fields': ('email', 'password1', 'password2'),
	    }),
	)
	readonly_fields=('user_hash',)
	form = ParticipantChangeForm
	add_form = ParticipantCreationForm
	change_password_form = AdminPasswordChangeForm
	list_display = ('email',)
	search_fields = ('email',)
	ordering = ('email',)
	# filter_horizontal = ('groups', 'user_permissions',)

	def get_fieldsets(self, request, obj=None):
	    if not obj:
	        return self.add_fieldsets
	    return super(ParticipantAdmin, self).get_fieldsets(request, obj)

	def get_form(self, request, obj=None, **kwargs):
	    """
	    Use special form during user creation
	    """
	    defaults = {}
	    if obj is None:
	        defaults['form'] = self.add_form
	    defaults.update(kwargs)
	    return super(ParticipantAdmin, self).get_form(request, obj, **defaults)

	def get_urls(self):
	    return [
	        url(r'^(\d+)/password/$', self.admin_site.admin_view(self.user_change_password)),
	    ] + super(ParticipantAdmin, self).get_urls()

	def lookup_allowed(self, lookup, value):
	    # See #20078: we don't want to allow any lookups involving passwords.
	    if lookup.startswith('password'):
	        return False
	    return super(ParticipantAdmin, self).lookup_allowed(lookup, value)
    
	@sensitive_post_parameters_m
	def user_change_password(self, request, id, form_url=''):
	    if not self.has_change_permission(request):
	        raise PermissionDenied
	    user = get_object_or_404(self.get_queryset(request), pk=id)
	    if request.method == 'POST':
	        form = self.change_password_form(user, request.POST)
	        if form.is_valid():
	            form.save()
	            change_message = self.construct_change_message(request, form, None)
	            self.log_change(request, user, change_message)
	            msg = ugettext('Password changed successfully.')
	            messages.success(request, msg)
	            update_session_auth_hash(request, form.user)
	            return HttpResponseRedirect('..')
	    else:
	        form = self.change_password_form(user)

	    fieldsets = [(None, {'fields': list(form.base_fields)})]
	    adminForm = admin.helpers.AdminForm(form, fieldsets, {})

	    context = {
	        'title': _('Change password: %s') % escape(user.get_username()),
	        'adminForm': adminForm,
	        'form_url': form_url,
	        'form': form,
	        'is_popup': (IS_POPUP_VAR in request.POST or
	                     IS_POPUP_VAR in request.GET),
	        'add': True,
	        'change': False,
	        'has_delete_permission': False,
	        'has_change_permission': True,
	        'has_absolute_url': False,
	        'opts': self.model._meta,
	        'original': user,
	        'save_as': False,
	        'show_save': True,
	    }
	    context.update(admin.site.each_context())
	    return TemplateResponse(request,
	        self.change_user_password_template or
	        'admin/auth/user/change_password.html',
	        context, current_app=self.admin_site.name)

	def response_add(self, request, obj, post_url_continue=None):
	    """
	    Determines the HttpResponse for the add_view stage. It mostly defers to
	    its superclass implementation but is customized because the User model
	    has a slightly different workflow.
	    """
	    # We should allow further modification of the user just added i.e. the
	    # 'Save' button should behave like the 'Save and continue editing'
	    # button except in two scenarios:
	    # * The user has pressed the 'Save and add another' button
	    # * We are adding a user in a popup
	    if '_addanother' not in request.POST and IS_POPUP_VAR not in request.POST:
	        request.POST['_continue'] = 1
	    return super(ParticipantAdmin, self).response_add(request, obj,
	                                               post_url_continue)

adminsite.register(OpTask, OpTaskAdmin)
adminsite.register(Product, ProductAdmin)
adminsite.register(TaskListItem, TaskListItemAdmin)
adminsite.register(Dataset)
adminsite.register(Participant, ParticipantAdmin)