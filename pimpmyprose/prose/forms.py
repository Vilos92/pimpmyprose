from prose.models import UserProfile, Prose, Pimp
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

# Form for submitting a prose
class ProseForm( forms.ModelForm ):
	prose_text = forms.CharField( widget = forms.Textarea( attrs = { 'class' : 'pimpProseSubmit' } ) )

	class Meta:
		model = Prose
		fields = ( 'prose_text', )

# Form for submitting a pimp
class PimpForm( forms.ModelForm ):
	pimp_text = forms.CharField( widget = forms.Textarea( attrs = { 'class' : 'pimpProseSubmit' } ) )

	class Meta:
		model = Pimp
		fields = ( 'pimp_text', )