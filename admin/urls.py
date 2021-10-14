from django.urls import path
from admin.views import Admin

urlpatterns = [
    path('', Admin.as_view()),
]