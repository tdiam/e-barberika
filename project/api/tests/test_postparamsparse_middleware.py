from django.test import TestCase, RequestFactory
from django.http import JsonResponse

from project.api.middleware import ParsePostParametersMiddleware

# A test view that returns the POST parameters parsed
def test_view(request):
    return JsonResponse(request.data)

class ParsePostParametersMiddlewareTestCase(TestCase):
    '''
    This is the test suite for the post parameters middleware.
    '''
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = ParsePostParametersMiddleware(test_view)

    # Check that params from POST indeed exist in `data`
    def test_form_parameters_are_accepted(self):
        request = self.factory.post('/', {'key': 'value'})
        self.middleware(request)

        # test that request.data gets created
        self.assertEqual(request.data['key'], 'value')

    # Check that params from body are parsed
    def test_urlencoded_parameters_are_accepted(self):
        # hack-y way to emulate x-www-form-urlencoded POST request (like curl)
        request = self.factory.post('/', content_type='application/x-www-form-urlencoded')
        request._body = b'key=value%20lit&list=31&list=32'
        self.middleware(request)

        self.assertEqual(request.data.get('key'), 'value lit')
        self.assertEqual(request.data.getlist('list'), ['31', '32'])