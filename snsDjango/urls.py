from django.urls import path
from . import views

app_name = 'snsDjango'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search', views.Search, name='search'), 
]
