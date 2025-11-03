from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Snippet
from django.core.exceptions import ObjectDoesNotExist


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)

def snippet_view_page(request, id: int):
    
    
    context = {'pagename': 'Просмотр сниппета'}
    try:
        snippet = Snippet.objects.get(pk=id)
    except ObjectDoesNotExist:
        return render(request, 'pages/error.html', context | {"error": f'Snippet with id={id} not found.'})
    else:
        context['snippet'] = snippet
        return render(request, 'pages/view_snippet.html', context)

def snippets_page(request):
    snippets = Snippet.objects.all().order_by('id')
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
        'all_snip': len(snippets),               
    }
    return render(request, 'pages/view_snippets.html', context)
