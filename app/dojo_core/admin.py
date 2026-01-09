from django.contrib import admin
from .models import (
    ConfiguracaoDojo,
    Aluno,
    Usuario,
    Presenca,
    ExameGraduacao,
    AtividadeExtra,
)

@admin.register(ConfiguracaoDojo)
class ConfiguracaoDojoAdmin(admin.ModelAdmin):
    list_display = ("nome_dojo", "duracao_aula_minutos", "criado_em", "atualizado_em")
    list_editable = ("duracao_aula_minutos",)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "faixa_atual", "data_cadastro")
    search_fields = ("nome", "email")
    list_filter = ("faixa_atual", "data_cadastro")
    ordering = ("nome",)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "tipo", "aluno", "criado_em")
    search_fields = ("nome", "email")
    list_filter = ("tipo",)
    ordering = ("nome",)


@admin.register(Presenca)
class PresencaAdmin(admin.ModelAdmin):
    list_display = ("id", "aluno", "data_aula", "duracao_minutos", "tipo_aula")
    list_filter = ("data_aula", "tipo_aula")
    search_fields = ("aluno__nome",)
    ordering = ("-data_aula",)


@admin.register(ExameGraduacao)
class ExameGraduacaoAdmin(admin.ModelAdmin):
    list_display = ("id", "aluno", "faixa_anterior", "faixa_nova", "data_exame")
    list_filter = ("faixa_nova", "data_exame")
    search_fields = ("aluno__nome",)
    ordering = ("-data_exame",)


@admin.register(AtividadeExtra)
class AtividadeExtraAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "aluno",
        "tipo_atividade",
        "data_inicio",
        "data_fim",
        "carga_horaria_minutos",
    )
    list_filter = ("tipo_atividade", "data_inicio")
    search_fields = ("aluno__nome",)
    ordering = ("-data_inicio",)
