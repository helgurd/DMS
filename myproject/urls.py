from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from myproject import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    url(r'^uploads/',include('gridfsuploads.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/',include('login.urls')),
    

    url('',RedirectView.as_view(url='/login/go/')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()

