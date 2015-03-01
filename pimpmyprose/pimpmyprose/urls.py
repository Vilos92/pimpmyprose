from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pimpmyprose.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url( r'^prose/', include( 'prose.urls', namespace = "prose" ) ),
    url( r'^admin/', include(admin.site.urls) ),
)

# Include urls for static files. Offline deployment
# Only works of DEBUG is True
urlpatterns += staticfiles_urlpatterns()