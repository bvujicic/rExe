from django.core.urlresolvers import resolve, reverse
from django.template import Library


register = Library()


@register.filter
def active_view(request, view_name):
    """
    Sets an HTML class attribute depending on the selection.

    :param request: HttpRequest
    :param view_name: (str)

    :return: (str) HTML class attribute
    """
    resolve_view_name = getattr(request.resolver_match, 'view_name', None)

    if resolve_view_name is not None and resolve_view_name.startswith(view_name):
        return 'active'
    else:
        return ''
