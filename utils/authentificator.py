from functools import wraps
from django.conf import settings
from hashlib import sha256

from django.http.response import HttpResponse


def need_auth(function):
    @wraps(function)
    def authentification_func(*args, **kwargs):
        if sha256(args[0].META['HTTP_ADMIN_PASSWORD']).hexdigest() == settings.HASHED_ADMIN_PASSWORD:
            result = function(*args, **kwargs)
            return result
        else:
            response = HttpResponse(
                "Authentification failed: header name should be Admin-Password and value equal to HASHED_ADMIN_PASSWORD in local_settings.py",
                content_type='application/json',
                status=401,
            )
            response['Access-Control-Allow-Origin'] = '*'
            return response
    return authentification_func
