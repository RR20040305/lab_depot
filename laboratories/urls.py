from django.urls import path
from . import views

urlpatterns = [
    path('', views.laboratories, name='laboratories'),
    path('<str:lab_id>/', views.laboratory_detail, name='laboratory_detail'),
]