from django.conf.urls import patterns, url

from prose import views


urlpatterns = patterns( '',
	# ex: /prose/
	url( r'^$', views.index, name = 'index' ),
	
	# ex: /prose/5/
	url( r'^(?P<prose_id>\d+)/$', views.detail, name = 'detail' ),
	
	# ex: /prose/5/results/
	url( r'^(?P<prose_id>\d+)/results/$', views.results, name = 'results' ),
	
	# ex: /prose/pimp/upvote/
	url( r'^upvote/$', views.upvote, name = 'upvote' ),
	
	# ex: /prose/pimp/10/downvote/
	url( r'^downvote/$', views.downvote, name = 'downvote' ),
	
	# ex: /prose/register/
	url( r'^register/$', views.register, name = 'register' ),
	
	# ex: /prose/login/
	url( r'^login/$', views.user_login, name = 'login' ),
	
	# ex: /prose/logout/
	url( r'^logout/$', views.user_logout, name = 'logout' ),
	
	# ex: /prose/profile/1/
	url( r'^profile/(?P<user_id>\d+)/$', views.profile, name = 'profile' ),
)