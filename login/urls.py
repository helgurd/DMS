from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^register/$', 'login.views.register', name='register'),
    url(r'^go/$', 'login.views.user_login', name='login'),
    url(r'^$',RedirectView.as_view(url='go/')),
    url(r'^success/$', 'login.views.success', name='login'),
    url(r'^logout/','login.views.logout_session', name='logout_session')
    )
