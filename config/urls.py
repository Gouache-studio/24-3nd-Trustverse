from django.urls import path, include

urlpatterns = [
    path('admin',include('admin.urls')),
    path('jupiter', include('jupiter.urls')),
    path('users', include('users.urls')),
    path('wallets', include('wallets.urls')),
]
