from django.contrib import admin
from django.urls import path, include
from app.dojo_core import views_admin
from dojo_core.views_admin import relatorios_home

urlpatterns = [
    path("admin/relatorios/", relatorios_home, name="admin-relatorios"),
    path("admin/", admin.site.urls),
    path("", include("dojo_core.urls")),
    path("admin/relatorios/ranking-assiduidade/", views_admin.ranking_assiduidade, name="ranking-assiduidade"),
]
