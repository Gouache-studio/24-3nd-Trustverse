from django.urls import path
from jupiter.views import ReportListView,ReportEditView,ReportDeleteView #,ReportUploadView

urlpatterns = [
    path("", ReportListView.as_view()),
    path("/edit", ReportEditView.as_view()),
    path("/delete", ReportDeleteView.as_view()),
    # path("/upload", ReportUploadView.as_view()),
]