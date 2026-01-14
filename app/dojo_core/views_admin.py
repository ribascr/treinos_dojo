from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from django.contrib import admin

@staff_member_required
def relatorios_home(request):
    context = {
        **admin.site.each_context(request),
        "title": "Relatórios",
    }
    return TemplateResponse(request, "admin/relatorios_home.html", context)