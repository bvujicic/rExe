from django.contrib import messages
from django.contrib.auth.views import (
    LoginView as BaseLoginView, LogoutView as BaseLogoutView, PasswordResetView as BasePasswordResetView,
    PasswordResetConfirmView as BasePasswordResetConfirmView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, CreateView, FormView, DetailView


from web.forms import AuthenticationForm, IterationCreateForm, RegistrationForm, PasswordResetForm, SetPasswordForm
from web.models import Iteration
from web.service import add_user_access


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

    def form_valid(self, form):
        user = form.save()
        add_user_access(user=user)

        messages.add_message(self.request, level=messages.INFO, message=_('Registracija uspješna.'))

        return super().form_valid(form)


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

    def get_queryset(self):
        """
        Renders Iterations specific to logged in user.
        """
        return super().get_queryset().filter(user=self.request.user)


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
