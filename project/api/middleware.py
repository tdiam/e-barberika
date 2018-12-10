from django.http import HttpResponseBadRequest

# Middleware to globally handle 'format' query parameter
# the default (and only supported) format is 'json', all others return 400 Bad Request
def ContentTypeMiddleware(get_response):

    def middleware(request):
        format_param = request.GET.get('format', 'json')

        if format_param != 'json':
            return HttpResponseBadRequest(f"Format {format_param} is not supported")

        # add ?format=json if not given explicitly
        # request.GET['format'] = format_param
        request.content_type = format_param

        return get_response(request)

    return middleware
