from django.urls import path
from .views import UploadReportView, GetReportsView

urlpatterns = [
    path("upload/", UploadReportView.as_view(), name="upload-report"),
    path("list/", GetReportsView.as_view(), name="get-reports"),
]
