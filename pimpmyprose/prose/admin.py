from django.contrib import admin
from prose.models import Prose, Pimp, UserProfile

class PimpInline( admin.TabularInline ):
	model = Pimp
	extra = 3

class ProseAdmin( admin.ModelAdmin ):
	fieldsets = [
		( None,					{ 'fields' : ['prose_text'] } ),
		( 'Date information',	{ 'fields' : ['pub_date'], 'classes' : ['collapse'] } ),
	]
	inlines = [PimpInline]
	list_display = ( 'prose_text', 'pub_date', 'was_published_recently' )
	list_filter = ['pub_date']
	search_fields = ['prose_text']
	
class PimpAdmin( admin.ModelAdmin ):
	fieldsets = [
		( None, { 'fields' : [ 'prose', 'pimp_text' ] } ),
		( 'Vote information',	{ 'fields' : [ 'upvotes', 'downvotes' ], 'classes' : ['collapse'] } ),
	]
	list_display = ( 'pimp_text', 'upvotes', 'downvotes' )

admin.site.register( Prose, ProseAdmin )
admin.site.register( Pimp, PimpAdmin )
admin.site.register( UserProfile )