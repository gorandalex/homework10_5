from django.urls import path
from . import views

app_name = 'quotes_app'

urlpatterns = [
    path('', views.quote_page, name='quote'),
    path('tag/<str:tag_name>/', views.tag_page, name='tag_page'),
    path('author/<str:author_name>/', views.author_detail, name='author_detail'),
    path('author_list/', views.author_list, name='author_list'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
]
