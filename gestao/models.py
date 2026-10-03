from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models

class Participante(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=25, blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Evento(models.Model):
    titulo = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    data = models.DateTimeField('data e horário')
    local = models.CharField(max_length=200)
    participantes = models.ManyToManyField(Participante, blank=True, related_name='eventos')

    class Meta:
        ordering = ['data']

    def __str__(self):
        return self.titulo

class Pagamento(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        PAGO = 'pago', 'Pago'

    participante = models.ForeignKey(Participante, on_delete=models.PROTECT, related_name='pagamentos')
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT, related_name='pagamentos')
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDENTE)
    vencimento = models.DateField()
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ['vencimento', 'pk']

    def __str__(self):
        return f'{self.participante} — {self.evento} ({self.get_status_display()})'

class Tarefa(models.Model):
    titulo = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    evento = models.ForeignKey(Evento, on_delete=models.SET_NULL, null=True, blank=True, related_name='tarefas')
    responsavel = models.ForeignKey(Participante, on_delete=models.SET_NULL, null=True, blank=True, related_name='tarefas')
    prazo = models.DateField(null=True, blank=True)
    concluida = models.BooleanField(default=False)

    class Meta:
        ordering = ['concluida', 'prazo', 'titulo']

    def __str__(self):
        return self.titulo
