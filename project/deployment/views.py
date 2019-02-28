from django.views import View
from django.http import HttpResponse
from django.conf import settings

class ReactAppView(View):
    '''redirect to react's `index.html`. Further routing is handled by React's router, we don't have to intervene'''

    def get(self, request, url=''):
        try:
            with open(settings.REACT_APP_INDEX_HTML, 'r') as index_html:
                return HttpResponse(index_html.read())
        except FileNotFoundError:
            return HttpResponse('React index.html file not found. Build react app first', status=501)
