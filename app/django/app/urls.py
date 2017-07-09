from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

import web.views as views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.LandingView.as_view(), name='landing'),
]

if settings.DEBUG:

    #from debug_toolbar import urls

    # urlpatterns.append(url(r'^__debug__/', include(urls)))
    urlpatterns.extend(staticfiles_urlpatterns())
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
