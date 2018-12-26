from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views import View

from .models import Token


def JsonMessageUtf8(msg, **kwargs):
    '''Returns JSON response {'message': msg} while not escaping UTF-8'''
    kwargs.setdefault('json_dumps_params', {})
    kwargs['json_dumps_params']['ensure_ascii'] = False
    return JsonResponse({'message': msg}, **kwargs)

class LoginView(View):
    '''Endpoint for users to obtain their API tokens.

    Users log in with their credentials: username and password.
    '''
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or password is None:
            return HttpResponseBadRequest('Τα πεδία username και password είναι υποχρεωτικά')

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


class LogoutView(View):
    '''
    Removes all tokens associated with `user`
    '''
    def post(self, request):
        if not hasattr(request, 'user'):
            # Logout when no user is logged in should not cause an error
            return HttpResponse(status=204)

        # remove tokens associated with this user
        Token.objects.filter(user=request.user).delete()

        return JsonMessageUtf8('OK')


class RegisterView(View):
    '''
    Registers a new user. Does not generate token
    '''
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or password is None:
            return JsonMessageUtf8('Τα πεδία username και password είναι υποχρεωτικά', status=400)

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            return JsonMessageUtf8(f'Το username {username} χρησιμοποιείται ήδη', status=400)

        User.objects.create_user(username=username, password=password)

        return JsonMessageUtf8('OK')
