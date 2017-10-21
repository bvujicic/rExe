from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

import web.views as views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^registracija$', views.RegisterView.as_view(), name='register'),
    url(r'^lozinka$', views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^lozinka/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),


    url(r'^algoritmi$', views.AlgorithmList.as_view(), name='algorithm_list'),
    url(
        r'^algoritmi/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$',
        views.AlgorithmDetail.as_view(),
        name='algorithm'
    ),
    url(r'^nova-obrada$', views.IterationCreateView.as_view(), name='iteration_create'),
    url(
        r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$',
        views.IterationView.as_view(),
        name='iteration'
    ),
    url(r'^$', views.HomeView.as_view(), name='home'),
]

if settings.DEBUG:

    #from debug_toolbar import urls

    # urlpatterns.append(url(r'^__debug__/', include(urls)))
    urlpatterns.extend(staticfiles_urlpatterns())
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
