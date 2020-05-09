from functools import wraps

from django.http import JsonResponse
from okta_jwt.jwt import validate_token, generate_token

from core.models import Config

config = Config()


def okta_login_required(func):
    @wraps(func)
    def wrap(request, *args, **kw):
        is_valid, message = check_token(request)
        if is_valid:
            return func(request, *args, **kw)
        else:
            return message

    return wrap


def check_token(request):
    access_token = request.META.get('HTTP_AUTHORIZATION')

    if access_token is None:
        return False, JsonResponse({"result": "HTTP_AUTHORIZATION required"}, status=400)

    try:
        validate_token(access_token, config.issuer, config.aud, config.client_id)
        return True, None

    except Exception as e:
        return False, JsonResponse({"result": e.args[0]}, status=400)
