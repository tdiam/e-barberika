from django.test import TestCase, RequestFactory
from django.http import JsonResponse

from project.api.middleware import ParseUrlEncodedParametersMiddleware

from .helpers import Request

# A test view
def test_view(request):
    return JsonResponse(request.data)

class ParseUrlEncodedParametersMiddlewareTestCase(TestCase):
    '''
    This is the test suite for the urlencoded parameters parser middleware.
    '''
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = ParseUrlEncodedParametersMiddleware(test_view)

    # Check `request.data` contains url encoded parameters
    def test_form_parameters_are_accepted(self):
        for i, method in enumerate(['get', 'post', 'put', 'patch', 'delete']):
            self.subTest(i)

            request = Request(method, '/', {'key': 'value'}, factory=self.factory)
            self.middleware(request)

            # test that `request.data` contains values
            self.assertEqual(request.data.get('key'), 'value')

    # Check `request.data` parses list
    def test_form_parameters_list_are_accepted(self):
        for i, method in enumerate(['get', 'post', 'put', 'patch', 'delete']):
            self.subTest(i)

            request = Request(method, '/', 'key=value&list=a&list=b', factory=self.factory)
            self.middleware(request)

            # test that `request.data` contains values
            self.assertEqual(request.data.get('key'), 'value')
            self.assertEqual(request.data.getlist('list'), ['a', 'b'])
