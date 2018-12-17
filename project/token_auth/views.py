from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views import View

from .models import Token


class ObtainTokenLoginView(View):
    '''Endpoint for users to obtain their API tokens.

    Users log in with their credentials: username and password.
    '''
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or password is None:
            return HttpResponseBadRequest('Both username and password are required')

        user = authenticate(request, username=username, password=password)

        # If authentication succeeded, return token
        if user is not None:
            # If user has obtained a token
            if hasattr(user, 'token'):
                token = user.token
            # If not
            else:
                # Generate one
                token = Token(user=user)
                token.save()
            return JsonResponse({'token': token.key})

        # If authentication failed, return 401.
        # Note: 401 responses typically need to be accompanied by a WWW-Authenticate header
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/WWW-Authenticate
        return HttpResponse('Unauthorized', status=401)
