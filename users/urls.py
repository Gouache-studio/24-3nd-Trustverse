from django.urls import path
from users.views import DashboardView, UserListView

urlpatterns = [
    path('', UserListView.as_view()),
    path('/dashboard', DashboardView.as_view())
]