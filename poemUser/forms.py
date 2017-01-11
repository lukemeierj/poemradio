from .models import PoemUser
from django.contrib.auth.models import User
from django import forms

#Old sign in protocol


# class UserForm(forms.ModelForm):
#     username = forms.CharField(max_length=30, label = "", widget = forms.TextInput(attrs={'placeholder': 'username'}))
#     class Meta:
#         model = User
#         labels = {'email': "", 'username':"", 'password':"", 'first_name':"", 'last_name':''}
#         widgets = {'password': forms.PasswordInput(attrs={'placeholder': 'password'}),
#                     'email': forms.TextInput(attrs={'placeholder': 'email'}),
#                     'first_name': forms.TextInput(attrs={'placeholder': 'first name'}),
#                     'last_name': forms.TextInput(attrs={'placeholder': 'last name'}),
#                     }
#         fields = ('email','username', 'password', 'first_name', 'last_name')



# class PoemUserForm(forms.ModelForm):
#     # preferences = forms.
#     class Meta:
#         model = PoemUser
#         # widgets = {'preferences': forms.CheckboxSelectMultiple()}
#         # fields = ('preferences', 'safeMode')
#         fields = ('safeMode',)

# class LogInForm(forms.Form):
# 	username = forms.CharField(max_length = 30, label = "", widget=forms.TextInput(attrs={'placeholder': 'username'}))
# 	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}), label = "")

# class SubmitPoemForm(forms.ModelForm):
# 	pass

class SignupForm(forms.Form):
    username = forms.CharField(max_length=30, label = '', widget = \
        forms.TextInput(attrs={'placeholder': 'username'}))
    first_name = forms.CharField(max_length=30, label = "", widget = \
        forms.TextInput(attrs={'placeholder': 'first'}))
    last_name = forms.CharField(max_length=30, label = "", widget = \
        forms.TextInput(attrs={'placeholder': 'last'}))
    safeMode = forms.BooleanField(label = "SafeMode (limit profanity)", required=False)
    tos = forms.BooleanField(label = "Agree to Privacy Policy and our Terms of Service", required=True)
    promo = forms.BooleanField(label = "Let us send you nifty emails once and a while", required = False, initial = True)


    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        tos = self.cleaned_data['tos']
        promo = self.cleaned_data['promo']
        safeMode      = self.cleaned_data['safeMode']
        poemUser      = PoemUser(user= user, agreed_tos = tos, promo_email = promo, safeMode = safeMode)
        poemUser.user = user
        poemUser.save()
        user.save()
        



        