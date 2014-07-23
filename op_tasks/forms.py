from models import *
from django.forms import ModelForm

from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django import forms

class ParticipantCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    email = forms.EmailField(label=_("Email"),
        help_text=_("Eg somename@somedomanin.com"),
        error_messages={'invalid': _("Please enter a valid email address.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Please reenter your password for confirmation"))

    class Meta:
        model = Participant
        fields = ("email",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            Participant._default_manager.get(email=email)
        except Participant.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(ParticipantCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        print 'CREATING USER, assigning operational tasks...'

        # get random product and associated dataset
        product = Product.objects.filter(is_active=True).order_by('?')[0]
        dataset = product.dataset

        # get random sequence of operational tasks
        operational_tasks = dataset.optask_set.filter(is_active=True).order_by('?')

        # assign it to the user
        setattr(user, 'product', product) 
        
        # if commit:
            user.save()

        # cycle through the operational tasks and assign to an index
        for ot_index, ot in enumerate(operational_tasks[0:3]):
            if ot_index==0:
                ot_active=True
            else:
                ot_active=False
            exit_active=False
            Sequence(user=user, op_task=ot, index=ot_index, ot_active=ot_active, exit_active=exit_active).save()
            print ot
        return user


class ParticipantChangeForm(forms.ModelForm):
    email = forms.EmailField(label=_("Email"),
        help_text=_("Required. dreed@test.com"),
        error_messages={
            'invalid': _("Please enter a valid email address.")})
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = Participant
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ParticipantChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]