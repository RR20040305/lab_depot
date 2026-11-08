from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('equipment/', include('equipment.urls')),
    path('laboratories/', include('laboratories.urls')),
    path('employees/', include('employees.urls')),
    path('issues/', include('issues.urls')),
]

# Подключение Debug Toolbar (если он установлен и DEBUG=True)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

handler404 = 'homepage.views.page_not_found'
