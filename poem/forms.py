from .models import Poem
from django.contrib.auth.models import User
from django import forms

class SubmitPoemForm(forms.ModelForm):
	class Meta:
		model = Poem
		widgets = {'tags': forms.CheckboxSelectMultiple()}
		# fields = ('title', 'text', 'source', 'tags')
		fields = ('title', 'text', 'source')