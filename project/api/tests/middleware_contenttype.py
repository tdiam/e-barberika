from django.test import TestCase, RequestFactory
from django.http import HttpResponse, Http404, HttpResponseBadRequest

from ..middleware import ContentTypeMiddleware
from ...settings import OBSERVATORY_API_ROOT

# A test view that returns 400 bad request if no ?format is given.
# otherwise it returns 200 ok along with the format name
def test_view(request):
    return HttpResponse(request.content_type)

def normal_view(request):
    return HttpResponse("ok")

class MiddlewareContentTypeTestCase(TestCase):
    '''
    This is the test suite for the content type middleware.
    We want `/?format=json` to be accepted, and all others
    rejected.

    Tests are based upon https://docs.djangoproject.com/en/2.1/topics/testing/advanced/#example
    '''

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = ContentTypeMiddleware(test_view)

        self.observatory_apiroot = OBSERVATORY_API_ROOT

    # Check that json is accepted and set properly
    def test_format_json_is_accepted(self):
        request = self.factory.get(self.observatory_apiroot, data={'format': 'json'})
        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(response.charset), 'json')

    # Check that xml returns 403 bad request
    def test_format_xml_is_not_accepted(self):
        request = self.factory.get(self.observatory_apiroot, data={'format': 'xml'})
        response = self.middleware(request)

        self.assertEqual(response.status_code, 400)

    # Check that format is accepted from url (json)
    def test_format_json_is_accepted_in_url(self):
        request = self.factory.get(self.observatory_apiroot + '?format=json')
        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(response.charset), 'json')

    # Check that the middleware only runs for the observatory, not all urls 
    def test_only_observatory_is_affected(self):
        middleware_for_default = ContentTypeMiddleware(normal_view)
        request = self.factory.get('/anything/?format=xml')
        response = middleware_for_default(request)

        self.assertEqual(response.status_code, 200)

    # Check that format defaults to json
    def test_default_format_works(self):
        request = self.factory.get(self.observatory_apiroot)
        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(response.charset), 'json')
