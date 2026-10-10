from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('equipment/', include('equipment.urls')),
    path('laboratories/', include('laboratories.urls')),
    path('employees/', include('employees.urls')),
    path('issues/', include('issues.urls')),
]

handler404 = 'homepage.views.page_not_found'