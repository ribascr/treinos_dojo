from django.db import models

class ConfiguracaoDojo(models.Model):
    nome_dojo = models.CharField(max_length=150, blank=True, null=True)
    duracao_aula_minutos = models.IntegerField(default=75)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_dojo or "Configuração do dojo"

class Faixa(models.Model):
    nome = models.CharField(max_length=50)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem"]

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    nome = models.CharField(max_length=150)
    data_nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    data_cadastro = models.DateField(auto_now_add=True)
    faixa_atual = models.ForeignKey(
    Faixa,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="alunos"
)
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Usuario(models.Model):
    TIPOS = (
        ("ADMIN", "Administrador"),
        ("ALUNO", "Aluno"),
    )
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    senha_hash = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=TIPOS, default="ALUNO")
    aluno = models.ForeignKey(Aluno, on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Presenca(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="presencas")
    data_aula = models.DateField()
    duracao_minutos = models.IntegerField()
    tipo_aula = models.CharField(max_length=100, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno.nome} - {self.data_aula}"


class ExameGraduacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="exames")
    faixa_anterior = models.CharField(max_length=50, blank=True, null=True)
    faixa_nova = models.CharField(max_length=50)
    data_exame = models.DateField()
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno.nome} - {self.faixa_nova}"


class AtividadeExtra(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="atividades_extras")
    tipo_atividade = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    carga_horaria_minutos = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno.nome} - {self.tipo_atividade}"

class Relatorios(models.Model):
    class Meta:
        managed = False
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios"

    def __str__(self):
        return "Relatórios"