from rest_framework import serializers
from .models import Aluno, Presenca, ExameGraduacao, AtividadeExtra

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = "__all__"


class PresencaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presenca
        fields = "__all__"


class ExameGraduacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExameGraduacao
        fields = "__all__"


class AtividadeExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtividadeExtra
        fields = "__all__"
