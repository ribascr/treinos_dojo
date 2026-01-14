from django.contrib import admin
from .admin import admin_site
from django.urls import path, include
from dojo_core.views_admin import relatorios_home

urlpatterns = [
    path("admin/relatorios/", relatorios_home, name="admin-relatorios"),
    path("admin/", admin.site.urls),
    path("", include("dojo_core.urls")),
]
