# helpers.py

from django.test import RequestFactory
from django.http import QueryDict

def Request(method: str, path: str, parameters, factory=None):
    '''
    Create a new request with url encoded parameters.
    If no request factory is given, a default is created.

    Returns `request` object.

    `parameters` can be either a dictionary or a urlencoded string.

    NOTE: {'list': ['a','b']} does not work, use urlencoded string for arrays
    '''
    method = method.lower()

    if method not in ['get', 'post', 'patch', 'put', 'delete']:
        raise ValueError("invalid HTTP method")

    if factory is None:
        factory = RequestFactory()

    # 'Post' ==> factory.post
    forge = getattr(factory, method.lower())
    request = forge(path)

    # url encode parameters and add to request body
    if isinstance(parameters, dict):
        qdict = QueryDict('', mutable=True)
        qdict.update(parameters)
        request._body = qdict.urlencode()
    elif isinstance(parameters, str):
        request._body = parameters
    else:
        raise ValueError('invalid parameters')

    # set content type, request factory does not always set it
    request.META['CONTENT_TYPE'] = 'application/x-www-form-urlencoded'

    return request
