from django.urls import path

from . import views

app_name = 'laboratories'

urlpatterns = [
    path('', views.laboratories, name='list'),
    path('<str:lab_id>/', views.laboratory_detail, name='detail'),
]