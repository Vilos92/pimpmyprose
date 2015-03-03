import datetime
import difflib

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

class UserProfile( models.Model ):
	user = models.OneToOneField( User, related_name = 'userProfile' )
	
	website = models.URLField( blank = True )
	
	def __unicode__(self):
		return self.user.username
		
	# Return all of this user's proses
	def getProses(self):
		return Prose.objects.filter( user = self.user )
	
	# Return all of this user's pimps
	def getPimps(self):
		return Pimp.objects.filter( user = self.user )

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