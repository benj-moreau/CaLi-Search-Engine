from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def index(request):
    return render(request, 'index.html')


@require_http_methods(['GET'])
def graph(request):
    return render(request, 'graph.html')


@require_http_methods(['GET'])
def search(request):
    return render(request, 'search.html')
