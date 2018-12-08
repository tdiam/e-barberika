from django.http import HttpResponseBadRequest

# Middleware to globally handle 'format' query parameter
# the default (and only supported) format is 'json', all others return 400 Bad Request
def ContentTypeMiddleware(get_response):

    def middleware(request):
        format_param = request.GET.get('format', d='json')

        if format_param != 'json':
            return HttpResponseBadRequest(f"Format {format_param} is not supported")

        return get_response(request)

    return middleware