import datetime
import difflib

from itertools import chain
from operator import attrgetter

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

class Prose( models.Model ):
	user = models.ForeignKey(User)
	prose_text = models.CharField( max_length = 250 )
	pub_date = models.DateTimeField( 'date published' )
	
	def __str__(self):
		return self.prose_text
		
	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta( days = 1 )
	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'
	
	# Return if a pimp already exists for this prose
	def pimpExists( self, pimp_text ):
		return self.pimp_set.filter( pimp_text = pimp_text ).count() > 0
	
	# Return all pimps ranked by their pimp score
	def rankedPimps(self):
		return sorted( list( self.pimp_set.all() ), key = lambda x : x.score, reverse = True )
	
	# Return culmative pimp score for this prose
	@property
	def pimpScoreSum(self):
		totScore = 0
		for pimp in self.pimp_set.all():
			totScore += pimp.score
		return totScore

class Pimp( models.Model ):
	user = models.ForeignKey(User)
 	prose = models.ForeignKey(Prose)
	pimp_text = models.CharField( max_length = 250 )
	pub_date = models.DateTimeField( 'date published' )
	
	# Upvotes and Downvotes many to many, must only let user
	# either upvote or downvote
	upvotes = models.ManyToManyField( User, null = True, blank = True, related_name = 'upvotedPimps' )
	downvotes = models.ManyToManyField( User, null  = True, blank = True, related_name = 'downvotedPimps' )
	
	def __str__(self):
		return self.pimp_text
	
	@property
	def score(self):
		return self.upvotes.count() - self.downvotes.count()
		
	# Return the difference of this Pimp from its parent Prose
	@property
	def percentMatch(self):
		# Get the seqence from Pimp and Prose texts
		seq = difflib.SequenceMatcher( None, self.prose.prose_text, self.pimp_text )
		
		# Get the percent match
		matchPercent = seq.ratio() * 100
		
		# Return the formatted percent match
		return int(matchPercent)

class UserProfile( models.Model ):
	user = models.OneToOneField( User, related_name = 'userProfile' )
	follows = models.ManyToManyField( 'self', related_name = 'followed_by' )
	
	# Notifications is a set of pimps (for now). No reason to add
	# a related_name field
	pimpNotifications = models.ManyToManyField(Pimp)
	
	def __unicode__(self):
		return self.user.username
		
	# Return all of this user's proses
	def getProses(self):
		return Prose.objects.filter( user = self.user )
	
	# Return all of this user's pimps
	def getPimps(self):
		return Pimp.objects.filter( user = self.user )

	# Return number of proses from user
	@property
	def getProsesAmt(self):
		return Prose.objects.filter( user = self.user ).count()
	
	# Return total prose score for user
	@property
	def getProseScore(self):
		allProse = Prose.objects.filter( user = self.user )
		totScore = 0
		for prose in allProse:
			totScore += prose.pimpScoreSum
		return totScore
	
	# Return number of pimps from user
	@property
	def getPimpsAmt(self):
		return Pimp.objects.filter( user = self.user ).count()
	
	# Return total pimp score for user
	@property
	def getPimpScore(self):
		allPimp = Pimp.objects.filter( user = self.user )
		totScore = 0
		for pimp in allPimp:
			totScore += pimp.score
		return totScore
	
	# Check if following another user
	def isFollowingUser( self, otherUser ):
		return self.follows.filter( pk = otherUser.userProfile.id ).exists()
		
	def isFollowingUserText( self, otherUser ):
		if self.isFollowingUser( otherUser ):
			return "Followed"
		else:
			return "Not Followed"
			
	# Return all pimp responses
	def getPimpResponses(self):
		allProses = self.getProses()
		
		# Get all proses from this
		pimp_response_set = []
		for prose in allProses:
			pimp_set = list( prose.pimp_set.all() )
			
			pimp_response_set = sorted(	chain( pimp_response_set, pimp_set ),
						key = attrgetter( 'pub_date' ), reverse = True )
						
		return pimp_response_set
			
	# Return notifications for user by pub_date, only 10
	def getPimpNotifications(self):
		return self.pimpNotifications.order_by('-pub_date')
		
	# Clear notifications before returning them
	def getClearPimpNotifications(self):
		pimp_notifications_list = list( self.getPimpNotifications() )
		self.pimpNotifications.clear()
		self.save()
		
		return pimp_notifications_list
		
	# Check if user has notifications
	@property
	def hasNotifications(self):
		return self.pimpNotifications.count() > 0
		
	# Check amount of notifications
	@property
	def getNotificationsCount(self):
		return self.pimpNotifications.count()
		
	# Follow or unfollow a user
	def followUserToggle( self, otherUser ):
		if self.isFollowingUser( otherUser ):
			self.follows.remove( otherUser.userProfile )
		else:
			self.follows.add( otherUser.userProfile )
		self.save()
		
		# Toggle does not return value, so option exists
		# To get either bool or text of isFollowing
		return None
		
	# Get amount of followers
	@property
	def getFollowersAmt(self):
		return self.follows.count()