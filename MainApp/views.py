from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from .models import Snippet, Comment
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index_page(request):

    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

@login_required
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
        if not snippet.is_public and (not request.user.is_authenticated or snippet.user != request.user):
            raise Http404(f"Snippet with id={id} not found")
    except ObjectDoesNotExist:
        return render(request, 'pages/error.html', context | {"error": f'Snippet with id={id} not found.'})
    else:
        context['snippet'] = snippet
        context['comment_form'] = CommentForm()
        return render(request, 'pages/view_snippet.html', context)

def snippets_page(request):
    Filtered_Snippets = Snippet.objects.filter(is_public=True).order_by('id')
    page_obj = Paginator(Filtered_Snippets, 20).get_page(request.GET.get('page'))
    context = {
        'pagename': 'Посмотреть сниппеты',
        'count': Filtered_Snippets.count(),
        'snippets': page_obj,
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
    
@login_required
def snippet_delete(request, id: int):
    if request.method == "GET" or request.method == "POST":
        snippet = get_object_or_404(Snippet, pk=id)
        snippet.delete()
    return redirect("view_snippets")

@login_required
def snippet_edit(request, id: int):
    snippet = get_object_or_404(Snippet, pk=id)
    if snippet.user != request.user:
        raise Http404("Snippet not found")

    if request.method == "POST":
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            next_url = request.GET.get("next") or reverse("my_snippets")
            return redirect(next_url)
    else:
        form = SnippetForm(instance=snippet)

    context = {
        "pagename": "Редактировать сниппет",
        "form": form,
    }

    return render(request, "pages/add_snippet.html", context)


def login_page(request):
    if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)
       else:
           context = {
               "pagename": "PythonBin",
               "errors"  : ["Incorrect username or password"]
           }
           return render(request, "pages/index.html", context)
    return redirect('home')

def logout_page(request):
    auth.logout(request)
    return redirect(to='home')

@login_required
def my_snippets_page(request):
    filtered_snippets = Snippet.objects.filter(user=request.user).order_by('id')
    page_obj = Paginator(filtered_snippets, 20).get_page(request.GET.get('page'))
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': page_obj,  
        'count': filtered_snippets.count(),  
    }
    return render(request, 'pages/view_snippets.html', context)

def create_user_page(request):

    context = {'pagename': 'Регистрация нового пользователя'}

    if request.method == "GET":
        form = UserRegistrationForm()
 
        return render(request, 'pages/registration.html', context={"form":form})
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    
    context["form"] = form
        
    return render(request, 'pages/registration.html', context)  

def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            snippet_id = request.POST.get("snippet_id")
            snippet = Snippet.objects.get(id=snippet_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
            return redirect("view_snippet", id=snippet_id)

    raise Http404    