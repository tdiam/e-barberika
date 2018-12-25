from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views import View

from .models import Token

def JSON_RESPONSE_400(msg):
    return JsonResponse({'status': msg}, json_dumps_params={'ensure_ascii': False}, status=400)

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


class TokenAuthLogoutView(View):
    '''
    Removes all tokens associated with `user`
    '''
    def post(self, request):
        if not getattr(request, 'user') or not request.user.is_authenticated:
            return HttpResponseForbidden() # REVIEW: maybe 401? 403 seems better

        # remove tokens associated with this user
        Token.objects.filter(user=request.user).delete()

        # REVIEW: anything that could go wrong?
        return JsonResponse({'message': 'OK'})

class TokenAuthRegisterView(View):
    '''
    Registers a new user. Does not generate token
    '''
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # REVIEW: other info?

        if username is None or password is None:
            return JSON_RESPONSE_400('Both username and password are required')

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            return JSON_RESPONSE_400(f'Το username `{username}` χρησιμοποιειται ηδη`')

        if User.objects.filter(email=email).exists():
            return JSON_RESPONSE_400(f'Το email `{email}` χρησιμοποιειται ηδη`')

        user = User.objects.create_user(username=username, password=password, email=email)
        # REVIEW: add to group?

        return JsonResponse({'status': 'OK'})
