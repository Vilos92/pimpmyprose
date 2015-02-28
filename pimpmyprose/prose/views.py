from django.shortcuts import get_object_or_404, render, render_to_response

from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from prose.models import Prose
from prose.forms import UserForm, UserProfileForm

def register(request):
	context = RequestContext(request)
	
	registered = False
	
	if request.method == 'POST':
		user_form = UserForm( data = request.POST )
		profile_form = UserProfileForm( data = request.POST )
		
		if user_form.is_valid() and profile_form.is_valid:
			# Save user data from form into user
			user = user_form.save()
			
			# Hash password and save user again
			user.set_password( user.password )
			user.save()
			
			profile = profile_form.save( commit = False )
			profile.user = user
			
			registered = True
		
		else:
			print user_form.errors, profile_form.errors
		
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response(
			'prose/register.html',
			{ 'user_form' : user_form, 'profile_form' : profile_form, 'registered' : registered },
			context )

def user_login(request):
	context = RequestContext(request)
	
	if request.method == 'POST':
	
		username = request.POST['username']
		password = request.POST['password']
		
		user= authenticate( username = username, password = password )
		
		if user:
			if user.is_active:
				login( request, user )
				return HttpResponseRedirect('/prose/')
			else:
				return HttpResponseRedirect( "Your pimpMyProse account is disabled." )
		else:
			print "Invalid login detail: {0}, {1}".format( username, password )
			return HttpResponse( "Invalid login details supplied." )
			
	else:
		return render_to_response( 'prose/login.html', {}, context )

@login_required
def user_logout(request):
	logout(request)
	
	return HttpResponseRedirect('/prose/')
		
def index(request):
	latest_prose_list = Prose.objects.order_by('-pub_date')[:5]
	context = { 'latest_prose_list' : latest_prose_list }
	return render( request, 'prose/index.html', context )
	
def detail( request, prose_id ):
	prose = get_object_or_404( Prose, pk = prose_id )
	return render( request, 'prose/detail.html', { 'prose' : prose } )
	
def results( request, prose_id ):
	respose = "You're looking at the results of prose %s."
	return HttpResponse( response % prose_id )

@login_required
def vote( request, prose_id ):
	return HttpResponse( "You're voting on prose %s." % prose_id )