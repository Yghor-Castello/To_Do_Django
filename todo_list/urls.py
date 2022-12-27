from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('accounts/', include('accounts.urls')), #CADASTRASNDO USUÁRIOS
    path('accounts/', include('django.contrib.auth.urls')), #INSERINDO AS URLS DE LOGIN DO DJANGO
]
