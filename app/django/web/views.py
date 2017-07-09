from django.contrib.auth.views import LoginView

from web.forms import AuthenticationForm


class LandingView(LoginView):
    """
    GET: Renders login form.
    POST: Processes form and logs user in.
    """
    #template_name = 'login.html'
    form_class = AuthenticationForm

    def get_template_names(self):

        if self.request.user.is_authenticated:
            return 'login.html'

        else:
            return 'home.html'
