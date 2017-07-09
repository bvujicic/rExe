from django.contrib.auth.views import LoginView

from web.forms import AuthenticationForm


class LandingView(LoginView):
    """
    GET: Renders login form.
    POST: Processes form and logs user in.
    """
    template_name = 'login.html'
    form_class = AuthenticationForm