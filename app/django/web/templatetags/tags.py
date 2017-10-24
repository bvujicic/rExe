import logging

from django.template import Node, Library, Variable
from django.utils.translation import get_language, activate, override

from django.core.urlresolvers import reverse_lazy, reverse

register = Library()

logger = logging.getLogger('web')


class TranslatedURL(Node):

    def __init__(self, required_language, view):
        self.required_language = Variable(required_language)
        self.view = Variable(view)

    def render(self, context):
        """
        Switches to the required language and calculates the URL with the required language selected.
        Switches back to request language.
        """
        try:
            view = self.view.resolve(context)
            language = self.required_language.resolve(context)

        except Exception as exc:
            logger.info('View context: {}'.format(self.view))
            return ''

        else:
            with override(language=language):
                if getattr(view, 'object', False):
                    url = view.object.get_absolute_url()
                else:
                    url = reverse(view.request.resolver_match.url_name, args=view.args, kwargs=view.kwargs)

            return url


@register.tag(name='translate_url')
def translated_url(parser, token):
    """
    Returns a translated URL.
    """
    return TranslatedURL(required_language=token.split_contents()[1], view=token.split_contents()[2])