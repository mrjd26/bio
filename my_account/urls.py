from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from emailusernames.forms import EmailAuthenticationForm

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.auth_login', name='login'),
    url(r'^registration/$', 'views.registration', name='registration'),
    url(r'^confirmed/$', 'views.confirmed', name='confirmed'),
    url(r'^logout/$', 'views.logout_view', name='logout'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^my_account/', include('bio.urls')),
)
