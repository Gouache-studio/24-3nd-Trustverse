from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin, auth

urlpatterns = [
    url(r'admin', admin.site.urls),
    # path('admin',include('admin.urls')),
    path('admincustom',include('admincustom.urls')),
    path('jupiter', include('jupiter.urls')),
    path('users', include('users.urls')),
    path('wallets', include('wallets.urls')),
]
