from django.urls import path
from jupiter.views import ReportListView

urlpatterns = [
    path("", ReportListView.as_view())
]