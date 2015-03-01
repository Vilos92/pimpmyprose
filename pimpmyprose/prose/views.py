from django.shortcuts import get_object_or_404, render, render_to_response

from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from prose.models import Prose, Pimp, UserProfile
from prose.forms import UserForm, UserProfileForm, ProseForm, PimpForm

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
			
			profile.save()
			
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
	context = RequestContext(request)
	
	if request.user.is_authenticated() and request.method == 'POST':
		prose_form = ProseForm( data = request.POST )
		
		if prose_form.is_valid():
			# Save prose data from form into prose
			prose = prose_form.save( commit = False )
			prose.user = request.user
			prose.pub_date = timezone.now()
			
			prose.save()
		
		else:
			print prose_form.errors
		
	else:
		prose_form = ProseForm()

	latest_prose_list = Prose.objects.order_by('-pub_date')[:5]
			
	return render_to_response(
			'prose/index.html',
			{ 'prose_form' : prose_form, 'latest_prose_list' : latest_prose_list  },
			context )
	
def detail( request, prose_id ):
	context = RequestContext(request)
	
	prose = get_object_or_404( Prose, pk = prose_id )
	
	if request.user.is_authenticated() and request.method == 'POST':
		pimp_form = PimpForm( data = request.POST )
		
		if pimp_form.is_valid():
			# Save prose data from form into prose
			pimp = pimp_form.save( commit = False )
			pimp.user = request.user
			pimp.pub_date = timezone.now()
			pimp.prose = prose
			
			pimp.save()
		
		else:
			print pimp_form.errors
		
	else:
		pimp_form = PimpForm()
		
	return render_to_response(
			'prose/detail.html',
			{ 'pimp_form' : pimp_form, 'prose' : prose },
			context )
	
def results( request, prose_id ):
	respose = "You're looking at the results of prose %s."
	return HttpResponse( response % prose_id )

@login_required
def vote( request, prose_id ):
	return HttpResponse( "You're voting on prose %s." % prose_id )
	
def profile( request, user_id ):
	context = RequestContext(request)

	user = get_object_or_404( User, pk = user_id )
	userProfile = user.userProfile
	
	# Need to get all proses for user
	latest_prose_list = Prose.objects.filter( user_id = user_id )[:5]
	
	# Need to get all pimps for user
	latest_pimp_list = Pimp.objects.filter( user_id = user_id )[:5]
	
	return render_to_response(
			'prose/profile.html',
			{ 'userProfile' : userProfile, 'latest_prose_list' : latest_prose_list, 'latest_pimp_list' : latest_pimp_list },
			context )