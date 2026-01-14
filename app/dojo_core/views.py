from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Aluno, Presenca, ExameGraduacao, AtividadeExtra, ConfiguracaoDojo
from .serializers import (
    AlunoSerializer,
    PresencaSerializer,
    ExameGraduacaoSerializer,
    AtividadeExtraSerializer,
)

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

        config = ConfiguracaoDojo.objects.first()
        duracao = config.duracao_aula_minutos if config else 75

        presenca = Presenca.objects.create(
            aluno=aluno,
            data_aula=now().date(),
            duracao_minutos=duracao,
        )
        return Response(PresencaSerializer(presenca).data, status=status.HTTP_201_CREATED)
from django.shortcuts import render, redirect, get_object_or_404
from .models import Aluno, Presenca, ConfiguracaoDojo
from django.utils.timezone import now

def aluno_dashboard(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    presencas = aluno.presencas.order_by("-data_aula")[:10]

    return render(request, "dojo_core/aluno_dashboard.html", {
        "aluno": aluno,
        "presencas": presencas,
    })


def registrar_presenca_page(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    hoje = now().date() 

    if request.method == "POST":
        # Verifica se já existe presença registrada hoje
        if Presenca.objects.filter(aluno=aluno, data_aula=hoje).exists():
            messages.error(request, "A presença de hoje já foi registrada.")
            return redirect("aluno-dashboard", aluno_id=aluno.id)

        # Obtém duração da aula
        config = ConfiguracaoDojo.objects.first()
        duracao = config.duracao_aula_minutos if config else 75

        # Cria a presença
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

