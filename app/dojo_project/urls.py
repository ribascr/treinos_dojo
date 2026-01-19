from django.contrib import admin
from django.urls import path, include
from dojo_core import views_admin
from dojo_core.views_admin import relatorios_home
from dojo_core.views import MeuLoginView


urlpatterns = [
    path("admin/relatorios/", relatorios_home, name="admin-relatorios"),
    path("admin/relatorios/ranking-assiduidade/", views_admin.ranking_assiduidade, name="ranking-assiduidade"),
    path("", include("dojo_core.urls")),
    path("admin/", admin.site.urls),   
    path('accounts/login/', MeuLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
]
