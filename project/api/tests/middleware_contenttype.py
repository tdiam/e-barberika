from django.test import TestCase, RequestFactory
from django.http import HttpResponse, Http404, HttpResponseBadRequest

from ..middleware import ContentTypeMiddleware

# A test view that returns 400 bad request if no ?format is given.
# otherwise it returns 200 ok along with the format name
def test_view(request):
    return HttpResponse(request.content_type)

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

    # Check that json is accepted and set properly
    def test_format_json_is_accepted(self):
        request = self.factory.get('/', data={'format': 'json'})
        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(response.charset), 'json')

    # Check that xml returns 403 bad request
    def test_format_xml_is_not_accepted(self):
        request = self.factory.get('/', data={'format': 'xml'})
        response = self.middleware(request)

        self.assertEqual(response.status_code, 400)

    # Check that format is accepted from url (json)
    def test_format_json_is_accepted_in_url(self):
        request = self.factory.get('/?format=json')
        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(response.charset), 'json')

    # Check that format is accepted from url (xml)
    def test_format_xml_is_not_accepted_in_url(self):
        request = self.factory.get('/?format=xml')
        response = self.middleware(request)

        self.assertEqual(response.status_code, 400)

    # Check that format defaults to json
    def test_default_format_works(self):
        request = self.factory.get('/')
        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(response.charset), 'json')
