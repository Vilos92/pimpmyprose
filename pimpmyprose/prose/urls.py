from django.conf.urls import patterns, url, include

from prose import views


urlpatterns = patterns( '',
	# ex: /prose/
	url( r'^$', views.index, name = 'index' ),
	# filtered ex: /prose/top/
	url( r'^(?P<filter>hot|top|new|worst|old)/$', views.index, name = 'index' ),

	# angularJS version of detail
	# ex: /prose_angular/5/
	url( r'^(?P<prose_id>\d+)/$', views.detail, name = 'detail' ),

	# ex: /prose/pimp/10/upvote/
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

	# All prose from a user
	# ex: /prose/profile/1/prose/
	url( r'^profile/(?P<user_id>\d+)/prose/$', views.profile_prose, name = 'profile_prose' ),

	# All pimps from a user
	# ex: /prose/profile/1/pimps/
	url( r'^profile/(?P<user_id>\d+)/pimps/$', views.profile_pimps, name = 'profile_pimps' ),

	# ex: /prose/profile/manage/
	url( r'^profile/manage/$', views.profile_manage, name = 'profile_manage' ),

	# Users a certain user is following
	# ex: /prose/profile/1/following
	url( r'^profile/(?P<user_id>\d+)/following/$', views.following, name = 'following' ),

	# Pimps from all users a user is following
	# ex: /prose/profile/1/following/pimps
	url( r'^profile/(?P<user_id>\d+)/following/pimps/$', views.following_pimps, name = 'following_pimps' ),

	# Prose from all users a user is following
	# ex: /prose/profile/1/following/prose
	url( r'^profile/(?P<user_id>\d+)/following/prose/$', views.following_prose, name = 'following_prose' ),

	# Users who are following a certain user
	# ex: /prose/profile/1/followers
	url( r'^profile/(?P<user_id>\d+)/followers/$', views.followers, name = 'followers' ),

	# ex: /prose/notifications/
	url( r'^notifications/$', views.notifications, name = 'notifications' ),

	# ex: /prose/follow/
	url( r'^follow/$', views.followToggle, name = 'follow' ),

	# ex: /prose/search
	url( r'^search/$', include( 'haystack.urls' ) ),
)
