from django.urls import path
from users.views import UserListView

urlpatterns = [
    path('', UserListView.as_view()),
]