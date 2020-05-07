from functools import wraps

from django.http import JsonResponse
from okta_jwt.jwt import validate_token, generate_token

from core.models import Config

config = Config()


def okta_login_required(func):
    @wraps(func)
    def wrap(request, *args, **kw):

        access_token = request.META.get('HTTP_AUTHORIZATION')

        if access_token is None:
            return JsonResponse({"result": "HTTP_AUTHORIZATION required"}, status=400)

        try:
            validate_token(access_token, config.issuer, config.aud, config.client_id)
            return func(request, *args, **kw)

        except Exception as e:
            return JsonResponse({"result": e.args[0]}, status=400)

    return wrap
