from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pimpmyprose.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url( r'^prose/', include( 'prose.urls', namespace = "prose" ) ),
    url( r'^admin/', include(admin.site.urls) ),
)
