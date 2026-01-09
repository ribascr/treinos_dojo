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
