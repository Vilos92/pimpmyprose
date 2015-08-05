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

# Rest Framework
from rest_framework import viewsets, permissions
from serializers import ProseSerializer, PimpSerializer
from permissions import IsOwnerOrReadOnly

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

# View to show all users another user is following
def following( request, user_id ):
	context = RequestContext(request)

	# Get the user profile to see who they are following
	user = get_object_or_404( User, pk = user_id )
	userProfile = user.userProfile

	# From this userProfile, get all users they are following
	following = userProfile.follows.all()

	# Pass users that are followed to the view
	return render_to_response(
			'prose/follows.html',
			{ 'userProfile' : userProfile, 'following' : following },
			context )

# Pimps from all users another user is following
def following_pimps( request, user_id ):
	context = RequestContext(request)

	# Get user profile to see who they are following
	user = get_object_or_404( User, pk = user_id )
	userProfile = user.userProfile

	# From this userProfile, get all users they are following
	following = userProfile.follows.all()

	# Get all pimps from the users being followed
	# To speed this up, try and have more of the filtering done by SQL
	# Need ability to sort based on URL
	following_pimps = []
	for followedUserProfile in following:
		pimps = followedUserProfile.getPimps().all()
		following_pimps.extend( pimps )

	# Want to show a link to the parent prose of each pimp
	show_parent_prose = True

	return render_to_response(
			'prose/follows_pimps.html',
			{ 'userProfile' : userProfile, 'following_pimps' : following_pimps, 'show_parent_prose' : show_parent_prose },
			context )

# Pimps from all users another user is following
def following_prose( request, user_id ):
	context = RequestContext(request)

	# Get user profile to see who they are following
	user = get_object_or_404( User, pk = user_id )
	userProfile = user.userProfile

	# From this userProfile, get all users they are following
	following = userProfile.follows.all()

	# Get all prose from the users being followed
	# To speed this up, try and have more of the filtering done by SQL
	# Need ability to sort based on URL
	following_prose = []
	for followedUserProfile in following:
		prose = followedUserProfile.getProses().all()
		following_prose.extend( prose )

	return render_to_response(
			'prose/follows_prose.html',
			{ 'userProfile' : userProfile, 'following_prose' : following_prose },
			context )

# View to show all users following a user
def followers( request, user_id ):
	context = RequestContext(request)

	# Get user profile to see their followers
	user = get_object_or_404( User, pk = user_id )
	userProfile = user.userProfile

	# From this userProfile, get all their followers
	followers = userProfile.followed_by.all()

	# Pass user's followers to the view
	return render_to_response(
			'prose/followers.html',
			{ 'userProfile' : userProfile, 'followers' : followers },
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

def detail_angular( request, prose_id ):
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

	return render_to_response(
			'prose/detail_angular.html',
			{ 'pimp_form' : pimp_form, 'prose' : prose },
			context )

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

# View a use profile, including self
def profile( request, user_id ):
	context = RequestContext(request)

	user = get_object_or_404( User, pk = user_id )
	userProfile = user.userProfile

	# Get 5 latest prose from user
	latest_prose_list = userProfile.getProses()[:5]

	# Get 5 latest pimps from user
	latest_pimp_list = userProfile.getPimps()[:5]

	# Pass pimp_list_profile as true to indicate that
	# pimps should have links to their parent prose
	show_parent_prose = True

	# Only show follow status if logged in
	followingUser = "Null"
	if request.user.is_authenticated():
		if request.user.userProfile.isFollowingUser( user ):
			followingUser = "Followed"
		else:
			followingUser = "Not Followed"

	return render_to_response(
			'prose/profile.html',
			{	'userProfile' : userProfile, 'prose_list' : latest_prose_list,
				'pimp_list' : latest_pimp_list, 'show_parent_prose' : show_parent_prose,
				'followingUser' : followingUser },
			context )

# View Prose of a user profile
def profile_prose( request, user_id ):
	context = RequestContext(request)

	user = get_object_or_404( User, pk = user_id )
	userProfile = user.userProfile

	# Get all prose from user
	prose_list = userProfile.getProses().all()

	return render_to_response(
			'prose/profile_prose.html',
			{ 'userProfile' : userProfile, 'prose_list' : prose_list },
			context )

# View Pimps of a user profile
def profile_pimps( request, user_id ):
	context = RequestContext(request)

	user = get_object_or_404( User, pk = user_id )
	userProfile = user.userProfile

	# Get all pimps from user
	pimp_list = userProfile.getPimps().all()

	# Pass pimp_list_profile as true to indicate that
	# pimps should have links to their parent prose
	show_parent_prose = True

	return render_to_response(
			'prose/profile_pimps.html',
			{ 'userProfile' : userProfile, 'pimp_list' : pimp_list },
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

#################################################
# REST Framework								#
#################################################
class ProseViewSet( viewsets.ModelViewSet ):
	"""
	API endpoint which allows Prose to be viewed or edited
	"""
	#queryset = Prose.objects.all()
	serializer_class = ProseSerializer

	def get_queryset(self):
		"""
		Restrict returned Prose to be from a specific user,
		by filtering against a 'username' query parameter in the URL
		"""
		queryset = Prose.objects.all()
		user_id = self.request.query_params.get( 'user_id', None )
		if user_id is not None:
			queryset = queryset.filter( user__id = user_id )
		return queryset

	permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
							IsOwnerOrReadOnly, )

class PimpViewSet( viewsets.ModelViewSet ):
	"""
	API endpoint which allows Pimps to be viewed or edited
	"""
	serializer_class = PimpSerializer

	def get_queryset(self):
		"""
		Restrict returned Pimps to be from a specific user,
		by filtering against a 'username' query parameter in the URL
		"""
		queryset = Pimp.objects.all()
		user_id = self.request.query_params.get( 'user_id', None )
		prose_id = self.request.query_params.get( 'prose_id', None )
		if user_id is not None:
			queryset = queryset.filter( user__id = user_id )
		elif prose_id is not None:
			queryset = queryset.filter( prose__id = prose_id )
		return queryset

	permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
							IsOwnerOrReadOnly, )
