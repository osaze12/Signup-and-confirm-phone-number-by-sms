from django.forms import ModelForm
from django.contrib.auth.models import User
from confBySms.models import Profile

from django import forms


class SignupForm(forms.ModelForm):
	first_name = forms.CharField(label="First name*", required=True)
	last_name = forms.CharField(label="Last name*", required=True)
	username = forms.CharField(label="Username*", required=True)
	email = forms.EmailField(label="Email*", required=True)
	day=forms.IntegerField()
	month=forms.CharField()
	year=forms.IntegerField()
	phone_number = forms.CharField(label="Phone Number*",required=True, initial= '+234')
	password = forms.CharField( label="Password*",widget=forms.PasswordInput, required=True)
	password2= forms.CharField(label="Confirm password*", widget=forms.PasswordInput, required=True)

	class Meta:
		model = User
		fields = ['first_name', 'last_name','username', 'email', 'password']
		widgets = {'password': forms.PasswordInput()}
		
	field_order = ['first_name', 'last_name', 'username', 'email', 'day',
	'month', 'year', 'phone_number', 'password', 'password2']



class ConfirmMe(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['token']


