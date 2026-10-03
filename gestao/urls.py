from django.urls import path
from . import views

app_name = 'gestao'
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('eventos/', views.eventos, name='eventos'),
    path('pagamentos/', views.pagamentos, name='pagamentos'),
]
