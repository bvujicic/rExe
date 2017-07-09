from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView

from web.forms import AuthenticationForm, IterationCreateForm
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


class HomeView(LoginRequiredMixin, ListView):
    """
    GET: Renders iteration listing for user.
    """
    template_name = 'home.html'
    model = Iteration

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.filter(user=self.request.user)


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