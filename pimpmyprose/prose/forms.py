from prose.models import UserProfile
from django.contrib.auth.models import User
from django import forms

class UserForm( forms.ModelForm ):
	password = forms.CharField( widget = forms.PasswordInput() )
	
	class Meta:
		model = User
		fields = ( 'username', 'email', 'password' )

# This will have more fields later
class UserProfileForm( forms.ModelForm ):
	class Meta:
		model = UserProfile
		fields = ( 'website', )