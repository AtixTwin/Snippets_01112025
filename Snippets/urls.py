from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name="home"),
    path('snippets/add', views.add_snippet_page, name="add_snippet"),
    path("snippets/<int:id>", views.snippet_view_page, name="view_snippet"),
    path("snippets/<int:id>/delete", views.snippet_delete_page, name="delete_snippet"),
    path("snippets/<int:id>/edit", views.snippet_edit_page, name="edit_snippet"),
    path('snippets/list', views.snippets_page, name="view_snippets"),
    # path("snippets/create", views.create_snippet_page, name="create_snippet"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('snippets/mine/', views.my_snippets_page, name='my_snippets'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
