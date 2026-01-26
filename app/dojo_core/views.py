from django.contrib import messages
from django.db.models import Sum
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import (
    Aluno,
    Presenca,
    ExameGraduacao,
    AtividadeExtra,
    ConfiguracaoDojo,
)

from .serializers import (
    AlunoSerializer,
    PresencaSerializer,
    ExameGraduacaoSerializer,
    AtividadeExtraSerializer,
)

class MeuLoginView(LoginView):
    template_name = 'accounts/login.html'
    def get_success_url(self):
        user = self.request.user
        aluno = Aluno.objects.filter(user=user).first()
        if aluno:
            return f'/aluno/{aluno.id}/'
        return '/'


# -----------------------------
# API VIEWSETS
# -----------------------------

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


class PresencaViewSet(viewsets.ModelViewSet):
    queryset = Presenca.objects.all()
    serializer_class = PresencaSerializer


class ExameGraduacaoViewSet(viewsets.ModelViewSet):
    queryset = ExameGraduacao.objects.all()
    serializer_class = ExameGraduacaoSerializer


class AtividadeExtraViewSet(viewsets.ModelViewSet):
    queryset = AtividadeExtra.objects.all()
    serializer_class = AtividadeExtraSerializer


class RegistrarPresencaViewSet(viewsets.ViewSet):
    def create(self, request, aluno_pk=None):
        try:
            aluno = Aluno.objects.get(pk=aluno_pk)
        except Aluno.DoesNotExist:
            return Response({"detail": "Aluno não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        hoje = now().date()

        # Impede duplicidade via API
        if Presenca.objects.filter(aluno=aluno, data_aula=hoje).exists():
            return Response(
                {"detail": "A presença de hoje já foi registrada."},
                status=status.HTTP_400_BAD_REQUEST
            )

        config = ConfiguracaoDojo.objects.first()
        duracao = config.duracao_aula_minutos if config else 75

        presenca = Presenca.objects.create(
            aluno=aluno,
            data_aula=hoje,
            duracao_minutos=duracao,
        )

        return Response(PresencaSerializer(presenca).data, status=status.HTTP_201_CREATED)


# -----------------------------
# HTML VIEWS
# -----------------------------

@login_required
def aluno_dashboard(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    presencas = aluno.presencas.order_by("-data_aula")[:10]

    total_minutos = aluno.presencas.aggregate(total=models.Sum("duracao_minutos"))["total"] or 0
    total_horas = round(total_minutos / 60, 2)

    return render(request, "dojo_core/aluno_dashboard.html", {
        "aluno": aluno,
        "presencas": presencas,
        "total_horas": total_horas,
    })

@login_required
def registrar_presenca_page(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    hoje = now().date()

    if request.method == "POST":
        if Presenca.objects.filter(aluno=aluno, data_aula=hoje).exists():
            messages.error(request, "A presença de hoje já foi registrada.")
            return redirect("aluno-dashboard", aluno_id=aluno.id)

        config = ConfiguracaoDojo.objects.first()
        duracao = config.duracao_aula_minutos if config else 75

        Presenca.objects.create(
            aluno=aluno,
            data_aula=hoje,
            duracao_minutos=duracao,
        )

        messages.success(request, "Presença registrada com sucesso.")
        return redirect("aluno-dashboard", aluno_id=aluno.id)

    return render(request, "dojo_core/registrar_presenca.html", {
        "aluno": aluno
    })
def ranking_assiduidade(request):
    ranking = (
        Aluno.objects
        .annotate(total_minutos=Sum("presencas__duracao_minutos"))
        .order_by("-total_minutos")
    )

    # Converte minutos para horas
    for aluno in ranking:
        aluno.total_horas = round((aluno.total_minutos or 0) / 60, 2)

    return render(request, "dojo_core/ranking_assiduidade.html", {
        "ranking": ranking
    })
