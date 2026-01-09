from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AlunoViewSet,
    PresencaViewSet,
    ExameGraduacaoViewSet,
    AtividadeExtraViewSet,
    RegistrarPresencaViewSet,
)

router = DefaultRouter()
router.register(r"alunos", AlunoViewSet, basename="aluno")
router.register(r"presencas", PresencaViewSet, basename="presenca")
router.register(r"exames", ExameGraduacaoViewSet, basename="exame")
router.register(r"atividades-extras", AtividadeExtraViewSet, basename="atividade-extra")

registrar_presenca = RegistrarPresencaViewSet.as_view({"post": "create"})

urlpatterns = [
    path("", include(router.urls)),
    path("alunos/<int:aluno_pk>/registrar-presenca/", registrar_presenca, name="registrar-presenca"),
]
