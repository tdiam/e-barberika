import urllib

from django.http import HttpResponseBadRequest, QueryDict
from django.conf import settings

# Middleware to globally handle 'format' query parameter
# the default (and only supported) format is 'json', all others return 400 Bad Request
def ObservatoryContentTypeMiddleware(get_response):

    def middleware(request):
        # only affect API calls to the observatory
        if not request.path.startswith(settings.API_ROOT):
            return get_response(request)

        format_param = request.GET.get('format', 'json')

        if format_param != 'json':
            return HttpResponseBadRequest(f"Format {format_param} is not supported")

        # add ?format=json if not given explicitly
        # request.GET['format'] = format_param
        request.content_type = format_param

        return get_response(request)

    return middleware


def ParsePostParametersMiddleware(get_response):
    '''
    Django by default does not parse POST parameters for requests with
        Content-Type: application/x-www-form-urlencoded
    This may be a problem, because some tools (e.g. `curl -X POST`) use this format

    As a solution, this middleware adds a new field to the request, `request.data`
    that correctly parses all POST parameters. `request.POST` remains unaffected

    REVIEW: should we just update the actual request.POST, instead of adding a new field?
    '''
    def middleware(request):

        # only for "Content-Type: x-www-form-urlencoded"
        if request.META['CONTENT_TYPE'] == 'application/x-www-form-urlencoded':
            # FIXME: this needs to be looked at
            request.data = QueryDict(request.body, mutable=False)
        elif request.method == 'POST':
            request.data = request.POST
        elif request.method == 'GET':
            request.data = request.GET

        return get_response(request)

    return middleware

