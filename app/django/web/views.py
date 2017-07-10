from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, CreateView, FormView, DetailView


from web.forms import AuthenticationForm, IterationCreateForm, RegistrationForm
from web.models import Iteration


class LoginView(BaseLoginView):
    """
    GET: Renders login form.
    POST: Processes form and logs user in.
    """
    template_name = 'login.html'
    form_class = AuthenticationForm


class LogoutView(BaseLogoutView):
    """
    GET: Log user out.
    """


class RegisterView(FormView):
    """
    GET:
    POST:
    """
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, level=messages.INFO, message=_('Potvrda o registracija poslana na e-mail.'))

        return super().form_valid(form)


class HomeView(LoginRequiredMixin, ListView):
    """
    GET: Renders iteration listing for user.
    """
    template_name = 'home.html'
    model = Iteration

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class IterationCreateView(LoginRequiredMixin, CreateView):
    """
    GET: Render form to create an iteration job.
    POST: Process form and create Iteration instance.
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
    GET: Renders Iteration details. Returns 403 if logged user is not related to Iteration.
    """
    template_name = 'iteration.html'
    model = Iteration
    raise_exception = True

    def test_func(self):
        if self.request.user == self.get_object().user:
            return True

        return False