from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Snippet


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)

def snippet_view_page(request, id: int):
    
    snippet = get_object_or_404(Snippet, pk=id)
    context = {
        'pagename': 'Просмотр сниппета',
        'snippet': snippet,
    }
    return render(request, 'pages/view_snippet.html', context)

def snippets_page(request):
    snippets = Snippet.objects.all().order_by('id')
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
        'all_snip': len(snippets),               
    }
    return render(request, 'pages/view_snippets.html', context)
