from prose.models import UserProfile, Prose, Pimp
from django.contrib.auth.models import User
from django import forms

class UserForm( forms.ModelForm ):
	password = forms.CharField( widget = forms.PasswordInput() )
	passwordValidate = forms.CharField( label = 'Validate Password', widget = forms.PasswordInput() )
	
	class Meta:
		model = User
		fields = ( 'username', 'email', 'password' )
	
	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter( username = username ).exists():
			raise forms.ValidationError( "Username already exists." )
		return username
	
	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter( email = email ).exists():
			raise forms.ValidationError( "Email already exists." )
		return email
			
	def clean(self):
		form_data = self.cleaned_data
		if form_data['password'] != form_data['passwordValidate']:
			self._errors['password'] = ['Password fields do not match.']
		return form_data

# This will have more fields later
class UserProfileForm( forms.ModelForm ):
	class Meta:
		model = UserProfile
		fields = ();

# Form for submitting a prose
class ProseForm( forms.ModelForm ):
	prose_text = forms.CharField( widget = forms.Textarea( attrs = { 'class' : 'pimpProseSubmit' } ), label = '' )

	class Meta:
		model = Prose
		fields = ( 'prose_text', )

# Form for submitting a pimp
class PimpForm( forms.ModelForm ):
	pimp_text = forms.CharField( widget = forms.Textarea( attrs = { 'class' : 'pimpProseSubmit' } ), label= '' )

	class Meta:
		model = Pimp
		fields = ( 'pimp_text', )