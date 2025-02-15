from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("Users.urls")),  # User authentication
    path("reports/", include("Reports.urls")),  # Reports app
]
