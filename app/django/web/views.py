from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from web.forms import AuthenticationForm
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