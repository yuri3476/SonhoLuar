# catalogo/admin.py
from django.contrib import admin
from .models import Produto, VariacaoProduto

# Permite editar Tamanhos/Estoque DENTRO da página do Produto
class VariacaoProdutoInline(admin.TabularInline):
    model = VariacaoProduto
    extra = 1 # Quantos campos extras mostrar
    autocomplete_fields = [] # Pode ser útil se tiver muitos tamanhos

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_base', 'disponivel')
    list_filter = ('disponivel',)
    search_fields = ('nome', 'descricao')
    inlines = [VariacaoProdutoInline] # ADICIONA O INLINE ACIMA