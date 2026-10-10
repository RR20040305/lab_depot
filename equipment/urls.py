from django.urls import path

from . import views

app_name = 'equipment'

urlpatterns = [
    path('', views.equipment, name='list'),
    path('<str:inv_num>/', views.equipment_detail, name='detail'),
]