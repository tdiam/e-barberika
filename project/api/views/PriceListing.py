## views for Price Listing endpoints

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest

import json

#################################################################

def prices_view_get(request):
    if request.method != 'GET':
        return HttpResponse(status_code=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest()

    ## TODO: do any model stuff
    return HttpResponse("placeholder")

def prices_view_post(request):
    # not really needed
    if request.method != 'POST':
        return HttpResponse(status_code=405)

    # TODO: authenticate user?

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest()

    return HttpResponse("placeholder")

#################################################################

# public
def prices_view(request):
    if request.method == 'GET':
        return prices_view_get(request)

    elif request.method == 'POST':
        return prices_view_post(request)

    return HttpResponse(status_code=405)