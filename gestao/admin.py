from django.contrib import admin
from .models import Evento, Pagamento, Participante, Tarefa

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'ativo')
    search_fields = ('nome', 'email')
    list_filter = ('ativo',)

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'local')
    search_fields = ('titulo', 'local')
    date_hierarchy = 'data'
    filter_horizontal = ('participantes',)

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('participante', 'evento', 'valor', 'status', 'vencimento')
    list_filter = ('status', 'evento')
    search_fields = ('participante__nome', 'evento__titulo')
    autocomplete_fields = ('participante', 'evento')

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'responsavel', 'evento', 'prazo', 'concluida')
    list_filter = ('concluida', 'evento')
    search_fields = ('titulo', 'responsavel__nome')
    autocomplete_fields = ('responsavel', 'evento')

admin.site.site_header = 'Gestão do Grupo de Jovens'
admin.site.site_title = 'Gestão do grupo'
admin.site.index_title = 'Cadastros e organização'
