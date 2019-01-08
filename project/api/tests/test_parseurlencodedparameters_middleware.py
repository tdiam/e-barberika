from unittest import skipIf

from django.test import TestCase
from django.http import HttpResponse
from django.conf import settings

from ..middleware import ParseUrlEncodedParametersMiddleware
from .helpers import ApiRequestFactory


def test_view(request):
    '''A test view.'''
    return HttpResponse(status=204)

class ParseUrlEncodedParametersMiddlewareTestCase(TestCase):
    '''
    This is the test suite for the urlencoded parameters parser middleware.
    '''
    def setUp(self):
        self.factory = ApiRequestFactory()
        self.middleware = ParseUrlEncodedParametersMiddleware(test_view)
        self.url = settings.API_ROOT

    @skipIf(settings.API_ROOT == '/', 'API_ROOT is "/", so all URLs are affected')
    def test_nonapi_url(self):
        '''Check if URLs not in API path do not contain `data` attribute.'''
        request = self.factory.post('/', {'key': 'value'})
        self.middleware(request)

        self.assertFalse(hasattr(request, 'data'))

    def test_form_parameters_are_accepted(self):
        '''Check `request.data` contains url encoded parameters'''
        for method in ['get', 'post', 'put', 'patch', 'delete']:
            with self.subTest(msg=f'method {method}'):
                forge = getattr(self.factory, method)
                request = forge(self.url, {'key': 'value'})
                self.middleware(request)

                # test that `request.data` contains values
                self.assertEqual(request.data.get('key'), 'value')

    def test_form_parameters_list_are_accepted(self):
        '''Check `request.data` parses list'''
        for method in ['get', 'post', 'put', 'patch', 'delete']:
            with self.subTest(msg=f'method {method}'):
                forge = getattr(self.factory, method)
                request = forge(self.url, {'key': 'value', 'list': ['a', 'b']})
                self.middleware(request)

                # test that `request.data` contains values
                self.assertEqual(request.data.get('key'), 'value')
                self.assertCountEqual(request.data.getlist('list'), ['a', 'b'])
