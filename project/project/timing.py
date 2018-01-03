import time

from django.utils.deprecation import MiddlewareMixin


class TimingMiddleware(object):
    """Times a request and adds timing information to the content.

    Adds an attribute, `_timing`, onto the request, and uses this at the end
    of the rendering chain to find the time difference. It replaces a token in
    the HTML, "<!-- RENDER_TIME -->", with the rendered time.
    """

    # Keep these out here so they can be modified in Django settings.

    REQUEST_ANNOTATION_KEY = "_timing"
    REPLACE = b"<!-- RENDER_TIME -->"
    REPLACE_TEMPLATE = b"<span>Handsomely rendered in %ims.</span>"

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        setattr(request, self.REQUEST_ANNOTATION_KEY, time.time())

        response = self.get_response(request)

        then = getattr(request, self.REQUEST_ANNOTATION_KEY, None)
        if then and hasattr(response, 'content'):
            now = time.time()
            msg = self.REPLACE_TEMPLATE % (int((now - then) * 1000))
            response.content = response.content.replace(self.REPLACE, msg)
        return response