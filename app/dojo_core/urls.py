from django.urls import path, include
from dojo_core.views_admin import relatorios_home
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    AlunoViewSet,
    PresencaViewSet,
    ExameGraduacaoViewSet,
    AtividadeExtraViewSet,
    RegistrarPresencaViewSet,
    aluno_dashboard,
    registrar_presenca_page,
)

router = DefaultRouter()
router.register(r"alunos", AlunoViewSet, basename="aluno")
router.register(r"presencas", PresencaViewSet, basename="presenca")
router.register(r"exames", ExameGraduacaoViewSet, basename="exame")
router.register(r"atividades-extras", AtividadeExtraViewSet, basename="atividade-extra")

registrar_presenca = RegistrarPresencaViewSet.as_view({"post": "create"})

urlpatterns = [
    # API
    path("", include(router.urls)),
    path("alunos/<int:aluno_pk>/registrar-presenca/", registrar_presenca, name="registrar-presenca-api"),

    # HTML
    path("aluno/<int:aluno_id>/", aluno_dashboard, name="aluno-dashboard"),
    path("aluno/<int:aluno_id>/registrar/", registrar_presenca_page, name="registrar-presenca"),
    path("admin/relatorios/", relatorios_home, name="admin-relatorios"),
    path("admin/", admin.site.urls),
]