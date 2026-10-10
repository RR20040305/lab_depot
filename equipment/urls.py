from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipment, name='equipment'),
    path('<str:inv_num>/', views.equipment_detail, name='equipment_detail'),
]