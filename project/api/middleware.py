from django.http import HttpResponseBadRequest, QueryDict
from django.conf import settings


def ObservatoryContentTypeMiddleware(get_response):
    '''Middleware to globally handle 'format' query parameter
    The default (and only supported) format is 'json', all others return 400 Bad Request.
    '''
    def middleware(request, *args, **kwargs):
        # only affect API calls to the observatory
        if not request.path.startswith(settings.API_ROOT):
            return get_response(request, *args, **kwargs)

        format_param = request.GET.get('format', 'json')

        if format_param != 'json':
            return HttpResponseBadRequest(f'Format {format_param} is not supported')

        # add ?format=json if not given explicitly
        # request.GET['format'] = format_param
        request.content_type = format_param

        return get_response(request, *args, **kwargs)

    return middleware


def ParseUrlEncodedParametersMiddleware(get_response):
    '''
    Parses request parameters in API calls and stores them in `request.data`.
    Django by default only parses request parameters when submitted via a form.
    Since our application works through API calls, we need this middleware that
    adds a new field to the request, `request.data` and correctly parses into it
    the urlencoded request parameters in the form of a QueryDict.
    QueryDict docs:
    https://docs.djangoproject.com/en/2.1/ref/request-response/#django.http.QueryDict
    '''
    def middleware(request, *args, **kwargs):
        # only affect API calls to the observatory
        if not request.path.startswith(settings.API_ROOT):
            return get_response(request, *args, **kwargs)

        request.data = QueryDict(request.body, mutable=True)
        # print('Middleware:', request._body, request.data)

        # Make GET parameters available in request.data too
        if request.method == 'GET':
            request.data.update(request.GET)

        return get_response(request, *args, **kwargs)

    return middleware
