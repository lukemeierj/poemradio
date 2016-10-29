from .models import PoemUser
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    class Meta:
        model = User
        widgets = {'password': forms.PasswordInput()}
        fields = ('email','username', 'password', 'first_name', 'last_name')



class PoemUserForm(forms.ModelForm):
    # preferences = forms.
    class Meta:
        model = PoemUser
        # widgets = {'preferences': forms.CheckboxSelectMultiple()}
        # fields = ('preferences', 'safeMode')
        fields = ('safeMode',)

class LogInForm(forms.Form):
	username = forms.CharField(max_length = 30)
	password = forms.CharField(widget=forms.PasswordInput())

class SubmitPoemForm(forms.ModelForm):
	pass