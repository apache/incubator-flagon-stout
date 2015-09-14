from django import forms

class DocumentForm(forms.Form):
	directory = forms.ChoiceField(
		choices=[('exp1', 'exp1'), ('exp2', 'exp2')]
	)
	docfile = forms.FileField(
		label='Select a file',
		help_text='max. 42 megabytes'
	)