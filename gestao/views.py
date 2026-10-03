from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import render
from .models import Evento, Pagamento, Participante, Tarefa
from django.db import models

@staff_member_required
def inicio(request):
    return render(request, 'gestao/inicio.html', {
        'participantes': Participante.objects.filter(ativo=True).count(),
        'eventos': Evento.objects.count(),
        'pagamentos_pendentes': Pagamento.objects.filter(status=Pagamento.Status.PENDENTE).count(),
        'tarefas_pendentes': Tarefa.objects.filter(concluida=False).count(),
        'lista_tarefas': (
            Tarefa.objects.filter(concluida=False)
            .select_related('responsavel', 'evento')
            .order_by(models.F('prazo').asc(nulls_last=True), 'pk')[:5]
        ),
    })

@staff_member_required
def eventos(request):
    return render(request, 'gestao/eventos.html', {'eventos': Evento.objects.prefetch_related('participantes')})

@staff_member_required
def pagamentos(request):
    registros = Pagamento.objects.select_related('participante', 'evento')
    totais = {status: registros.filter(status=status).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
              for status in (Pagamento.Status.PAGO, Pagamento.Status.PENDENTE)}
    return render(request, 'gestao/pagamentos.html', {'pagamentos': registros, 'totais': totais})
