from django.urls import path
from . import views

app_name = 'issues'

urlpatterns = [
    path('', views.issues, name='list'),
    path('statistics/', views.statistics, name='statistics'),
    path('<int:issue_id>/', views.issue_detail, name='detail'),
]
