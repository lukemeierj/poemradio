from .models import Poem
from django.contrib.auth.models import User
from django import forms

class SubmitPoemForm(forms.ModelForm):
	title = forms.CharField(label = "", widget= forms.TextInput(attrs={'placeholder': 'title'}))
	text = forms.CharField(label = "", widget= forms.Textarea(attrs={'placeholder': 'put your poetry in this box'}))
	source = forms.CharField(label = "", required = False, widget= forms.TextInput(attrs={'placeholder': 'Source URL'}))
	centered = forms.BooleanField(label = "", required = False, initial = False)
	
	class Meta:
		model = Poem
		# fields = ('title', 'text', 'source', 'tags')
		fields = ('title', 'text', 'source', 'centered')