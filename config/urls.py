from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('academics/', include('academics.urls')),
    path('planner/', include('planner.urls')),
    path('practice/', include('practice.urls')),
    path('revision/', include('revision.urls')),
    path('assistant/', include('assistant.urls')),
]
