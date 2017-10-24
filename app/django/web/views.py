from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import (
    LoginView as BaseLoginView, LogoutView as BaseLogoutView, PasswordResetView as BasePasswordResetView,
    PasswordResetConfirmView as BasePasswordResetConfirmView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.db.transaction import atomic
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView, CreateView, FormView, DetailView, View
from django.utils.translation import ugettext_lazy as _

from web.forms import AuthenticationForm, IterationCreateForm, RegistrationForm, PasswordResetForm, SetPasswordForm
from web.models import Iteration, Algorithm
from web.service import add_user_access, send_activation_mail, verify_activation_token


class LoginView(BaseLoginView):
    """
    GET: Renders login form.
    POST: Processes form and logs User in.
    """
    template_name = 'users/login.html'
    form_class = AuthenticationForm


class LogoutView(BaseLogoutView):
    """
    GET: Log user out.
    """


class RegisterView(FormView):
    """
    GET: Renders registration form.
    POST: Processes registration form and creates and persists a User instance.
    """
    template_name = 'users/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    @atomic
    def form_valid(self, form):
        user = form.save()
        add_user_access(user=user)
        send_activation_mail(request=self.request, user=user)

        messages.add_message(
            self.request,
            level=messages.INFO,
            message=_('Registracija uspješna. E-mail za aktivaciju poslan na {}.'.format(user.email))
        )
        return super().form_valid(form)


class RegisterConfirmView(View):
    """
    GET: Verifies activation token and activates the user. Redirects appropriately.
    """
    def get(self, request, *args, **kwargs):
        token = self.kwargs.get('token', None)
        uidb64 = self.kwargs.get('uidb64', None)

        user_verified = verify_activation_token(uidb64=uidb64, token=token)

        if user_verified:
            messages.add_message(self.request, level=messages.INFO, message=_('Aktivacija uspješna.'))

            return HttpResponseRedirect(redirect_to=settings.LOGIN_URL)

        else:
            raise Http404


class PasswordResetView(BasePasswordResetView):
    """
    GET: Renders password reset form email.
    POST: Processes form and send a reset link.
    """
    template_name = 'users/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.add_message(self.request, level=messages.INFO, message=_('Aktivacijski link poslan na e-mail adresu.'))

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, level=messages.ERROR, message=_('Nepostojeća e-mail adresa.'))

        return super().form_invalid(form)


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    """
    GET: Renders password change form.
    POST: Processes form and resets password.
    """
    INTERNAL_RESET_URL_TOKEN = 'nova'
    template_name = 'users/password_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.add_message(self.request, level=messages.INFO, message=_('Lozinka promijenjena.'))

        return super().form_valid(form)


class HomeView(LoginRequiredMixin, ListView):
    """
    GET: Renders iteration listing for user.
    """
    template_name = 'home.html'
    model = Iteration
    context_object_name = 'iteration_list'

    def get_queryset(self):
        """
        Renders Iterations specific to logged in user.
        """
        return super().get_queryset().filter(user=self.request.user)


class AlgorithmList(LoginRequiredMixin, ListView):
    """
    GET: Renders submenu with algoritm listings.
    """
    template_name = 'home.html'
    model = Algorithm
    context_object_name = 'algorithm_list'

    def get_queryset(self):
        return super().get_queryset().filter(users=self.request.user, is_active=True)


class AlgorithmDetail(LoginRequiredMixin, DetailView):
    """
    GET: Renders submenu with algoritm listings.
    """
    template_name = 'algorithm.html'
    model = Algorithm

    def get_queryset(self):
        return super().get_queryset().filter(users=self.request.user, is_active=True)


class IterationCreateView(LoginRequiredMixin, CreateView):
    """
    GET: Renders form to create Iteration.
    POST: Processes form and creates Iteration instance.
    """
    template_name = 'create_iteration.html'
    model = Iteration
    form_class = IterationCreateForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs


class IterationView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    GET: Renders Iteration details. Returns 403 if logged user is not parent to Iteration.
    """
    template_name = 'iteration.html'
    model = Iteration
    raise_exception = True

    def test_func(self):
        if self.request.user == self.get_object().user:
            return True

        return False
