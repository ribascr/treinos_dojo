from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from dojo_core import views_admin
from django.contrib import admin
from django.shortcuts import render
from django.db.models import Sum
from dojo_core.models import Aluno, Presenca

def ranking_assiduidade(request):
    ranking = (
        Aluno.objects
        .annotate(horas_treinadas=Sum("presencas__duracao"))
        .order_by("-horas_treinadas")
    )

    return render(
        request,
        "admin/ranking_assiduidade.html",
        {"ranking": ranking}
    )

@staff_member_required
def relatorios_home(request):
    context = {
        **admin.site.each_context(request),
        "title": "Relatórios",
    }
    return TemplateResponse(request, "admin/relatorios_home.html", context)