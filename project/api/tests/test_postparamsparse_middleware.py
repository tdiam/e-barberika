from django.test import TestCase, RequestFactory
from django.http import JsonResponse

from project.api.middleware import ParsePostParametersMiddleware

# A test view that returns the POST parameters parsed
def test_view(request):
    return JsonResponse(request.Post)

class ParsePostParametersMiddlewareTestCase(TestCase):
    '''
    This is the test suite for the post parameters middleware.
    '''
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = ParsePostParametersMiddleware(test_view)

    # Check that params from POST indeed exist in Post
    def test_form_parameters_are_accepted(self):
        request = self.factory.post('/', {'key': 'value'})
        self.middleware(request)

        # test that request.Post gets created
        self.assertEqual(request.Post['key'], 'value')

    # Check that params from body are parsed
    def test_urlencoded_parameters_are_accepted(self):
        # hack-y way to emulate x-ww-form-urlencoded POST request (like curl)
        request = self.factory.post('/', content_type='application/x-www-form-urlencoded')
        request._body = b'key=value&list=31&list=32'
        self.middleware(request)

        self.assertEqual(request.Post['key'], 'value')
        self.assertEqual(set(request.Post['list']), set(['32', '31']))

    # # Check that params may co-exist
    # def test_merge_correctly(self):
    #     request = self.factory.post('/', {'key':'value', 'list':'a'})
    #     request.body = b'list=b&other=hey'
    #     self.middleware(request)

    #     self.assertEqual(request.Post['key'], 'value')
    #     self.assertEqual(request.Post['list'], ['a','b'])
    #     self.assertEqual(request.Post['other'], 'hey')
