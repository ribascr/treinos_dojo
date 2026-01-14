from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from dojo_core import views_admin
from django.contrib import admin
from django.shortcuts import render
from django.db.models import Sum, Count, F, ExpressionWrapper, FloatField, ExpressionWrapper
from dojo_core.models import Aluno, Presenca

def ranking_assiduidade(request):
    ano = request.GET.get("ano")
    mes = request.GET.get("mes")

    presencas = Presenca.objects.all()

    if ano:
        presencas = presencas.filter(data_aula__year=ano)

    if mes:
        presencas = presencas.filter(data_aula__month=mes)

    total_aulas_periodo = presencas.values("data_aula").distinct().count()
    if total_aulas_periodo == 0:
        total_aulas_periodo = 1

    ranking = (
        Aluno.objects
        .annotate(
            total_minutos=Sum("presencas__duracao_minutos", filter=presencas.filter(aluno=F("id"))),
            total_presencas=Count("presencas", filter=presencas.filter(aluno=F("id")))
        )
        .annotate(
            porcentagem=ExpressionWrapper(
                F("total_presencas") * 100.0 / total_aulas_periodo,
                output_field=FloatField()
            )
        )
        .order_by("-total_minutos")
    )

    # Dados para o gráfico
    labels = [aluno.nome for aluno in ranking]
    horas = [(aluno.total_minutos or 0) / 60 for aluno in ranking]
    porcentagens = [aluno.porcentagem or 0 for aluno in ranking]

    return render(
        request,
        "admin/ranking_assiduidade.html",
        {
            "ranking": ranking,
            "ano": ano,
            "mes": mes,
            "labels": labels,
            "horas": horas,
            "porcentagens": porcentagens,
        }
    )

@staff_member_required
def relatorios_home(request):
    context = {
        **admin.site.each_context(request),
        "title": "Relatórios",
    }
    return TemplateResponse(request, "admin/relatorios_home.html", context)