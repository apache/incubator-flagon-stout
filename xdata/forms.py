from django import forms

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, MultiField, Div
# from crispy_forms.bootstrap import FormActions, PrependedText



class ExampleForm(forms.Form):
    like_website = forms.TypedChoiceField(
        label = "Do you like this website?",
        choices = ((1, "Yes"), (0, "No")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,
    )

    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = True,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = True,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    notes = forms.CharField(
        label = "Additional notes or feedback",
        required = False,
    )
    def __init__(self, *args, **kwargs):
        super(ExampleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            MultiField(
		        'Tell us your favorite stuff {{ email }}',
		        Div(
		            'like_website',
		            'favorite_number',
		            css_id = 'special-fields'
		        ),
		        PrependedText('favorite_color', '@', placeholder="email"),
		        'favorite_food',
		        'notes'
		    ),
            FormActions(
			    Submit('save', 'Save changes'),
			    Button('cancel', 'Cancel')
			)
        )

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

CHOICES=[('select1','select 1'),
         ('select2','select 2')]

class QuestionForm(forms.Form):    
    borrower = forms.CharField(label='Borrower')
    id = forms.CharField(label='ID #')

