from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

from neomodels.models import LicenseModel, DatasetModel


@require_http_methods(['GET'])
def test(request):
    license = LicenseModel(label='test')
    license.save()
    response = HttpResponse(
        "bonjour",
        content_type='charset=utf-8')
    response['Access-Control-Allow-Origin'] = '*'
    return response
