import datetime

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

class UserProfile( models.Model ):
	user = models.OneToOneField( User, related_name = 'userProfile' )
	
	website = models.URLField( blank = True )
	
	def __unicode__(self):
		return self.user.username

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
	
class Pimp( models.Model ):
	user = models.ForeignKey(User)
 	prose = models.ForeignKey(Prose)
	pimp_text = models.CharField( max_length = 250 )
	pub_date = models.DateTimeField( 'date published' )
	upvotes = models.IntegerField( default = 0 )
	downvotes = models.IntegerField ( default = 0 )
	
	def __str__(self):
		return self.pimp_text