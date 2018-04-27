from django.conf import settings

BOOTSTRAP_PAGINATION_URL_STARTINGS = getattr(settings, 'BOOTSTRAP_PAGINATION_URL_STARTINGS', None)
if BOOTSTRAP_PAGINATION_URL_STARTINGS:
    BOOTSTRAP_PAGINATION_URL_STARTINGS = BOOTSTRAP_PAGINATION_URL_STARTINGS.split(',')

try:
    from django.utils.deprecation import MiddlewareMixin
    object = MiddlewareMixin
except:
    pass


def get_page(self):
    """
    A function which will be monkeypatched onto the request to get the current
    integer representing the current page.
    """
    try:
        return int(self.GET.get('page'))
    except (KeyError, ValueError, TypeError):
        return 1


class PaginationMiddleware(object):
    """
    Inserts a variable representing the current page onto the request object if
    it exists in either **GET** or **POST** portions of the request.
    """
    def process_request(self, request):
        if BOOTSTRAP_PAGINATION_URL_STARTINGS:
            path = request.path
            for start in BOOTSTRAP_PAGINATION_URL_STARTINGS:
                if path.startswith(start):
                    request.__class__.page = property(get_page)
                    return
        page = getattr(request.__class__, 'page', None)
        if page is not None and 'property' in str(type(page)):
            request.__class__.page = None

