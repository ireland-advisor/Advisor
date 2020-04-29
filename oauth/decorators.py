
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse


def okta_login_required(func):
    def wrapper(request, *args, **kw):
        if 'tokens' not in request.session:
            if request.method == 'POST':
                response = HttpResponse()
                response.status_code = 401
                return response
            else:
                return JsonResponse({
                     "status": False,
                     "message": "please login"
                })
        else:
            return func(request, *args, **kw)

    return wrapper
