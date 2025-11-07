from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.forms import SnippetForm
from .models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth




def index_page(request):

    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):

    if request.method == "GET":
        form = SnippetForm(initial={"lang": "py"})
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form,
            }   
        return render(request, 'pages/add_snippet.html', context)
    
    if request.method == "POST":
        form = SnippetForm(request.POST, initial={"lang": "py"})
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("view_snippets")
        return render(request, 'pages/add_snippet.html', context={"form":form})  
      
    
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
    }
    return render(request, 'pages/view_snippets.html', context)

# def create_snippet_page(request):
#     if request.method == "POST":
#         form = SnippetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("view_snippets")
#         return render(request, 'pages/add_snippet.html', context={"form":form})  
      
#     return HttpResponseNotAllowed(['POST'],'Something goes wrong...: you must make POST request!')
    

def snippet_delete_page(request, id: int):
    if request.method == "GET" or request.method == "POST":
        snippet = get_object_or_404(Snippet, pk=id)
        snippet.delete()
    return redirect("view_snippets")

def snippet_edit_page(request, id: int):
    pass


def login_page(request):
    if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       # print("username =", username)
       # print("password =", password)
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)
       else:
           # Return error message
           pass
    return redirect('home')

def logout_page(request):
    auth.logout(request)
    return redirect(to='home')