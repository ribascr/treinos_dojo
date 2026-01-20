from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from dojo_core import views_admin
from django.contrib import admin
from django.shortcuts import render
from django.db.models import Sum, Count, F, ExpressionWrapper, FloatField, ExpressionWrapper, Q
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
            total_minutos=Sum(
                "presencas__duracao_minutos",
                filter=Q(presencas__in=presencas)
            ),
            total_presencas=Count(
                "presencas",
                filter=Q(presencas__in=presencas)
            )
        )
        .annotate(
            porcentagem=ExpressionWrapper(
                F("total_presencas") * 100.0 / total_aulas_periodo,
                output_field=FloatField()
            )
        )
        .order_by("-total_minutos")
    )

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
def relatorio_horas_treinadas(request):
    ano = request.GET.get("ano")
    mes = request.GET.get("mes")

    presencas = Presenca.objects.all()

    if ano:
        presencas = presencas.filter(data_aula__year=ano)

    if mes:
        presencas = presencas.filter(data_aula__month=mes)

    ranking = (
        Aluno.objects
        .annotate(
            total_minutos=Sum(
                "presencas__duracao_minutos",
                filter=Q(presencas__in=presencas)
            )
        )
        .annotate(
            total_horas=ExpressionWrapper(
                F("total_minutos") / 60.0,
                output_field=FloatField()
            )
        )
        .order_by("-total_horas")
    )

    labels = [aluno.nome for aluno in ranking]
    horas = [aluno.total_horas or 0 for aluno in ranking]

    return render(
        request,
        "admin/relatorio_horas_treinadas.html",
        {
            "ranking": ranking,
            "ano": ano,
            "mes": mes,
            "labels": labels,
            "horas": horas,
        }
    )

@staff_member_required
def relatorio_alunos_por_faixa(request):
    dados = (
        Aluno.objects
        .values("faixa_atual")
        .annotate(total=Count("id"))
        .order_by("faixa_atual")
    )

    labels = [item["faixa_atual"] for item in dados]
    totais = [item["total"] for item in dados]

    return render(
        request,
        "admin/relatorio_alunos_por_faixa.html",
        {
            "dados": dados,
            "labels": labels,
            "totais": totais,
        }
    )


@staff_member_required
def relatorios_home(request):
    context = {
        **admin.site.each_context(request),
        "title": "Relatórios",
    }
    return TemplateResponse(request, "admin/relatorios_home.html", context)