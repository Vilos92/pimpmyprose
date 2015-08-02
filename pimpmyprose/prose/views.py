import datetime

from django.shortcuts import get_object_or_404, render, render_to_response

from django.template import RequestContext

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from prose.models import Prose, Pimp, UserProfile
from prose.forms import UserForm, UserProfileForm, UserManageForm, ProseForm, PimpForm

# Include custom functions for hot ranking (from reddit)
from ranking_functions import getHotScore

def register(request):
	context = RequestContext(request)

	if ( request.user.is_authenticated() ):
		return render_to_response(
				'prose/register.html',
				{},
				context )

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

			# Log user in
			userLogin = authenticate( username = request.POST['username'], password = request.POST['password'] )
			login( request, userLogin)

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

	# No need to do anything else if user is already authenticated
	# Maybe just redirect to index
	if ( request.user.is_authenticated() ):
		return render_to_response( 'prose/login.html', {}, context )

	if request.method == 'POST':

		username = request.POST['username']
		password = request.POST['password']

		user = authenticate( username = username, password = password )

		if user:
			if user.is_active:
				login( request, user )
				return HttpResponseRedirect( reverse( 'prose:index' ) )
			else:
				return HttpResponseRedirect( "Your pimpMyProse account is disabled." )
		else:
			print "Invalid login detail: {0}, {1}".format( username, password )
			return render_to_response( 'prose/login.html', { 'invalidLogin' : True }, context )

	else:
		return render_to_response( 'prose/login.html', {}, context )

@login_required
def user_logout(request):
	logout(request)

	return HttpResponseRedirect( reverse( 'prose:index' ) )

def index( request, filter = 'hot' ):
	context = RequestContext(request)

	# Allow user to post Prose from index
	if request.user.is_authenticated() and request.method == 'POST':
		prose_form = ProseForm( data = request.POST )

		if prose_form.is_valid():
			# Save prose data from form into prose
			prose = prose_form.save( commit = False )
			# Reset prose form so no data on page reload
			prose_form = ProseForm()

			prose.user = request.user
			prose.pub_date = timezone.now()

			prose.save()

			# Redirect to the detail for this newly created Prose
			return HttpResponseRedirect( reverse( 'prose:detail', args = [ prose.id ] ) )

		else:
			print prose_form.errors

	else:
		prose_form = ProseForm()

	# Create empty set of prose for case of bad filter input
	prose_list = []
	# Sort by filter, default is hot
	if filter == 'hot':
		# Should not get all and then sort by hot, need to either store
		# hot rating in database to speed up loading or stick to newest 200
		# Replace this later by adding time to score for rank (lke reddit)
		prose_list = Prose.objects.all()[:200]
		prose_list = sorted( list( prose_list ), key = lambda x : getHotScore( x.pimpScoreSum, datetime.datetime.now() ) , reverse = True )
	# Sort by filter, default is top
	elif filter == 'top':
		# Best of all time. Should have sub-filter for how long ago (like reddit)
		prose_list = Prose.objects.all()
		prose_list = sorted( list( prose_list ), key = lambda x : x.pimpScoreSum, reverse = True )
	elif filter == 'new':
		# Simply get the 50 latest posts
		prose_list = Prose.objects.order_by('-pub_date')[:50]
	elif filter == 'worst':
		# Show worst posts
		prose_list = Prose.objects.order_by('-pub_date')[:50]
		prose_list = sorted( list( prose_list ), key = lambda x : x.pimpScoreSum )
	elif filter == 'old':
		prose_list = Prose.objects.order_by('pub_date')[:50]

	return render_to_response(
			'prose/index.html',
			{ 'prose_form' : prose_form, 'prose_list' : prose_list, 'filter' : filter },
			context )

def detail( request, prose_id, filter = 'top' ):
	context = RequestContext(request)

	prose = get_object_or_404( Prose, pk = prose_id )

	if request.user.is_authenticated() and request.method == 'POST':
		pimp_form = PimpForm( data = request.POST )

		if pimp_form.is_valid():
			# Check to see if pimp already exists for this prose
			pimp_text = pimp_form.cleaned_data['pimp_text']
			if prose.pimpExists( pimp_text ):
				# If pimp already exists, return normal PimpForm and error
				pimp_form = PimpForm()
				pimp_form.errors["pimp_text"] = ErrorList( [u"Pimp already exists."] )

			# Pimp does not exist, create and save
			else:
				# Save prose data from form into prose
				pimp = pimp_form.save( commit = False )
				# Reset pimp form for page reload, no repost
				pimp_form = PimpForm()

				pimp.user = request.user
				pimp.pub_date = timezone.now()
				pimp.prose = prose

				# Must save before m2m value can be added
				pimp.save()

				# Set current user to be an upvoter
				pimp.upvotes.add( request.user )

				# Final save
				pimp.save()

				# Also, notify the prose user that someone pimped his prose
				prose.user.userProfile.pimpNotifications.add(pimp)
				prose.save()

		else:
			print pimp_form.errors

	else:
		pimp_form = PimpForm()

	# Create empty rankedPimps object
	rankedPimps = []
	# Sort by filter, default is top
	if filter == 'top':
		rankedPimps = prose.rankedPimps()
	elif filter == 'new':
		rankedPimps = prose.newPimps()
	elif filter == 'worst':
		rankedPimps = prose.worstPimps()
	elif filter == 'old':
		rankedPimps = prose.oldPimps()

	return render_to_response(
			'prose/detail.html',
			{ 'pimp_form' : pimp_form, 'prose' : prose, 'pimp_list' : rankedPimps, 'filter' : filter },
			context )

def results( request, prose_id ):
	respose = "You're looking at the results of prose %s."
	return HttpResponse( response % prose_id )

@login_required
def upvote(request):
	context = RequestContext(request)
	pimp_id = None
	if request.method == 'POST':
		pimp_id = request.POST.get( 'pimp_id' )

	pimp = get_object_or_404( Pimp, pk = pimp_id )

	pimp.downvotes.remove( request.user )
	if pimp.upvotes.filter( pk = request.user.id ):
		pimp.upvotes.remove( request.user )
	else:
		pimp.upvotes.add( request.user )

	pimp.save()

	# Return the new score to be redisplayed
	return HttpResponse( pimp.score )

@login_required
def downvote( request ):
	context = RequestContext(request)
	pimp_id = None
	if request.method == 'POST':
		pimp_id = request.POST.get('pimp_id')

	pimp = get_object_or_404( Pimp, pk = pimp_id )

	pimp.upvotes.remove( request.user )
	if pimp.downvotes.filter( pk = request.user.id ):
		pimp.downvotes.remove( request.user )
	else:
		pimp.downvotes.add( request.user )

	pimp.save()

	# Return the new score to be redisplayed
	return HttpResponse( pimp.score )

def profile( request, user_id ):
	context = RequestContext(request)

	user = get_object_or_404( User, pk = user_id )
	userProfile = user.userProfile

	# Need to get all proses for user
	latest_prose_list = userProfile.getProses()[:5]

	# Need to get all pimps for user
	latest_pimp_list = userProfile.getPimps()[:5]

	# Pass pimp_list_profile as true to indicate that
	# pimps should have links to their parent prose
	show_parent_prose = True

	# Only show follow status if logged in
	if request.user.is_authenticated():
		if request.user.userProfile.isFollowingUser( user ):
			followingUser = "Followed"
		else:
			followingUser = "Not Followed"
	else:
		followingUser = "Null"

	return render_to_response(
			'prose/profile.html',
			{	'userProfile' : userProfile, 'prose_list' : latest_prose_list,
				'pimp_list' : latest_pimp_list, 'show_parent_prose' : show_parent_prose,
				'followingUser' : followingUser },
			context )

# View current user's notifications
@login_required
def notifications(request):
	context = RequestContext(request)

	# Show notifications
	pimp_notification_list = request.user.userProfile.getClearPimpNotifications()

	# Get all user pimp responses
	pimp_response_list = request.user.userProfile.getPimpResponses()

	# Subtract notification list from the overall pimp_response_list
	pimp_response_list = [ pimp for pimp in pimp_response_list if pimp not in pimp_notification_list ]

	# Pass variable to indicate that Pimp's should link to their parent Prose
	show_parent_prose = True

	return render_to_response(
			'prose/notifications.html',
			{ 'pimp_notification_list' : pimp_notification_list, 'pimp_response_list' : pimp_response_list, 'show_parent_prose' : show_parent_prose },
			context )

# Manage the user profile
@login_required
def profile_manage( request ):
	context = RequestContext(request)

	if request.method == 'POST':
		# Edited Form to allow passing in request, to allow user to keep email
		userManage_form = UserManageForm( data = request.POST, user = request.user )

		if userManage_form.is_valid():
			currUser = User.objects.get( pk = request.user.id )

			# Save info from form into user
			currUser.email = request.POST['email']

			if not request.POST['password'] == '':
				currUser.set_password( request.POST['password'] )

			currUser.save()

			# Log user in
			userLogin = authenticate( username = request.user.username, password = request.POST['password'] )
			login( request, userLogin)

			# Add message to flash message telling user profile edited
			messages.add_message( request, messages.INFO, 'Profile Updated' )

		else:
			print userManage_form.errors

	else:
		userManage_form = UserManageForm()

	return render_to_response(
			'prose/profile_manage.html',
			{ 'userManage_form' : userManage_form },
			context )

# View to toggle following status, works with ajax. Returns text
@login_required
def followToggle( request ):
	context = RequestContext(request)

	user_id = None
	if request.method == 'POST':
		user_id = request.POST.get( 'user_id' )

	otherUser = get_object_or_404( User, pk = user_id )

	thisUser = request.user.userProfile

	# Toggle follow on the other user
	thisUser.followUserToggle( otherUser )

	# Return whether following or not as bool, parse on other side into text
	return HttpResponse( thisUser.isFollowingUserText( otherUser ) )
