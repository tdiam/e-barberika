from django.test import RequestFactory
from django.utils.http import urlencode


API_CONTENT_TYPE = 'application/x-www-form-urlencoded'

class ApiRequestFactory(RequestFactory):
    '''
    RequestFactory for our API.

    This is a subclass of RequestFactory that uses application/x-www-form-urlencoded
    as the default content type for GET, POST, PATCH, PUT and DELETE, and encodes
    data as URL encoded parameters.
    '''
    def generic(self, method, path, data='',
                content_type=API_CONTENT_TYPE, secure=False, **kwargs):
        '''Generic handler of all request methods.'''
        # Convert dictionary to URL encoded string
        if content_type == API_CONTENT_TYPE and isinstance(data, dict):
            # Set doseq=True, otherwise {'a': ['b', 'c']} would be
            # converted to "a=['b',+'c']" instead of "a=b&a=c".
            data = urlencode(data, doseq=True)
        return super().generic(method, path, data, **kwargs)

    def get(self, path, data=None, secure=False, **kwargs):
        '''Construct a GET request.

        GET requests don't use the body anyway, so just call the get
        method of the superclass and only change the content type.
        '''
        kwargs.setdefault('content_type', API_CONTENT_TYPE)
        return super().get(path, data, secure, **kwargs)

    def post(self, path, data=None, content_type=API_CONTENT_TYPE,
             secure=False, **kwargs):
        '''Construct a POST request.'''
        return self.generic('POST', path, data, content_type, secure=secure, **kwargs)

    def patch(self, path, data='', content_type=API_CONTENT_TYPE,
              secure=False, **kwargs):
        '''Construct a PATCH request.'''
        return self.generic('PATCH', path, data, content_type, secure=secure, **kwargs)

    def put(self, path, data='', content_type=API_CONTENT_TYPE,
            secure=False, **kwargs):
        '''Construct a PUT request.'''
        return self.generic('PUT', path, data, content_type, secure=secure, **kwargs)

    def delete(self, path, data='', content_type=API_CONTENT_TYPE,
               secure=False, **kwargs):
        '''Construct a DELETE request.'''
        return self.generic('DELETE', path, data, content_type, secure=secure, **kwargs)
