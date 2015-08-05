from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Imports for Django Rest Framework
from rest_framework import routers
from prose import views

# Register routers for Prose and Pimp views
router = routers.DefaultRouter()
router.register( r'prose', views.ProseViewSet, base_name = 'prose' )
router.register( r'pimp', views.PimpViewSet, base_name = 'pimp' )

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pimpmyprose.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url( r'^', include( 'prose.urls', namespace = "prose" ) ),
    url( r'^admin/', include(admin.site.urls) ),

	# Urls for Django Rest Framework
	url( r'^api/', include( router.urls ) ),
	url( r'^api-auth/', include( 'rest_framework.urls', namespace = 'rest_framework' ) ),
)

# Include urls for static files. Offline deployment
# Only works of DEBUG is True
urlpatterns += staticfiles_urlpatterns()
