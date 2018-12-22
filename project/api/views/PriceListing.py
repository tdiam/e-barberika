## views for Price Listing endpoints

import json

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views import View



#################################################################

# public
class PricesView(View):
    def get(self, request):
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest()

        ## TODO: do any model stuff
        return HttpResponse("placeholder")

    def post(self, request):
        # TODO: authenticate user?

        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest()

        return HttpResponse("placeholder")