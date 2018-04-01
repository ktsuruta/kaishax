from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:edinet_code>/', views.detail, name='detail'),
]
