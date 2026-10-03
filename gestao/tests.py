from datetime import date
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Evento, Pagamento, Participante, Tarefa

class GestaoTests(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user('equipe', password='teste-local-123', is_staff=True)
        self.participante = Participante.objects.create(nome='Pessoa de exemplo')
        self.evento = Evento.objects.create(titulo='Encontro de exemplo', data=timezone.now(), local='Salão')
        self.evento.participantes.add(self.participante)

    def test_consultas_exigem_equipe(self):
        for nome in ('inicio', 'eventos', 'pagamentos'):
            self.assertRedirects(self.client.get(reverse(f'gestao:{nome}')),
                                 '/admin/login/?next=' + reverse(f'gestao:{nome}'))
        comum = get_user_model().objects.create_user('comum', password='teste-local-123')
        self.client.force_login(comum)
        self.assertEqual(self.client.get(reverse('gestao:pagamentos')).status_code, 302)

    def test_telas_e_totais(self):
        for status, valor in [('pago', '25.50'), ('pendente', '10.00')]:
            Pagamento.objects.create(participante=self.participante, evento=self.evento,
                                     valor=valor, status=status, vencimento=date.today())
        Tarefa.objects.create(titulo='Organizar sala', responsavel=self.participante)
        self.client.force_login(self.usuario)
        inicio = self.client.get(reverse('gestao:inicio'))
        self.assertEqual(inicio.status_code, 200)
        self.assertEqual(inicio.context['tarefas_pendentes'], 1)
        self.assertContains(self.client.get(reverse('gestao:eventos')), self.evento.titulo)
        resposta = self.client.get(reverse('gestao:pagamentos'))
        self.assertContains(resposta, self.participante.nome)
        self.assertEqual(resposta.context['totais']['pago'], Decimal('25.50'))
        self.assertEqual(resposta.context['totais']['pendente'], Decimal('10.00'))

    def test_pagamento_valor_e_protecao(self):
        pagamento = Pagamento(participante=self.participante, evento=self.evento,
                              valor=Decimal('-1'), vencimento=date.today())
        with self.assertRaises(ValidationError):
            pagamento.full_clean()
        pagamento.valor = Decimal('1.00')
        pagamento.full_clean()
        pagamento.save()
        with self.assertRaises(ProtectedError):
            self.participante.delete()
        with self.assertRaises(ProtectedError):
            self.evento.delete()

    def test_telas_vazias(self):
        self.evento.delete()
        self.client.force_login(self.usuario)
        self.assertContains(self.client.get(reverse('gestao:eventos')), 'Nenhum evento cadastrado')
        self.assertContains(self.client.get(reverse('gestao:pagamentos')), 'Nenhum pagamento registrado')
