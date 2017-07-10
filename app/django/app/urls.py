from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

import web.views as views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^registracija/$', views.RegisterView.as_view(), name='register'),
    url(r'^nova-obrada/$', views.IterationCreateView.as_view(), name='iteration_create'),
    url(r'^$', views.HomeView.as_view(), name='home'),
]

if settings.DEBUG:

    #from debug_toolbar import urls

    # urlpatterns.append(url(r'^__debug__/', include(urls)))
    urlpatterns.extend(staticfiles_urlpatterns())
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
