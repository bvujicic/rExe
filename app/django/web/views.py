from django.contrib.auth.views import LoginView


class LandingView(LoginView):
    """
    GET: Renders login form.
    POST: Processes form and logs user in.
    """
    template_name = 'login.html'