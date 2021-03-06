from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

import web.views as views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rosetta/', include('rosetta.urls'))
]

urlpatterns += i18n_patterns(
    url(
        format_lazy(r'^{0}$', pgettext_lazy('Dio URL-a', 'login')),
        views.LoginView.as_view(),
        name='login'
    ),
    url(
        format_lazy(r'^{0}$', pgettext_lazy('Dio URL-a', 'logout')),
        views.LogoutView.as_view(),
        name='logout'
    ),
    url(
        format_lazy(r'^{0}$', pgettext_lazy('Dio URL-a', 'registracija')),
        views.RegisterView.as_view(),
        name='register'
    ),
    url(
        # doubles braces to avoid clash between regex syntax and python formatting
        format_lazy(
            r'^{0}/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{{1,13}}-[0-9A-Za-z]{{1,20}})$',
            pgettext_lazy('Dio URL-a', 'registracija')
        ),
        views.RegisterConfirmView.as_view(),
        name='register_confirm'
    ),
    url(
        format_lazy(r'^{0}$', pgettext_lazy('Dio URL-a', 'lozinka')),
        views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    url(
        format_lazy(
            r'^{0}/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{{1,13}}-[0-9A-Za-z]{{1,20}})$',
            pgettext_lazy('Dio URL-a', 'lozinka')
        ),
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    url(
        format_lazy(r'^{0}$', pgettext_lazy('Dio URL-a', 'algoritmi')),
        views.AlgorithmList.as_view(),
        name='algorithm_list'
    ),
    url(
        format_lazy(
            r'^{0}/(?P<pk>[0-9a-f]{{8}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{12}})$',
            pgettext_lazy('Dio URL-a', 'algoritmi')
        ),
        views.AlgorithmDetail.as_view(),
        name='algorithm'
    ),
    url(
        format_lazy(r'^{0}$', pgettext_lazy('Dio URL-a', 'nova-obrada')),
        views.IterationCreateView.as_view(),
        name='iteration_create'
    ),
    url(
        r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$',
        views.IterationView.as_view(),
        name='iteration'
    ),
    url(r'^$', views.HomeView.as_view(), name='home'),
)

if settings.DEBUG:

    #from debug_toolbar import urls

    # urlpatterns.append(url(r'^__debug__/', include(urls)))
    urlpatterns.extend(staticfiles_urlpatterns())
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
