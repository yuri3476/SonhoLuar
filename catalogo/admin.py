# catalogo/admin.py
from django.contrib import admin
from .models import Produto, VariacaoProduto, ImagemProduto # <--- IMPORTE O NOVO MODELO

# ... (Sua classe VariacaoProdutoInline continua igual) ...
class VariacaoProdutoInline(admin.TabularInline):
    model = VariacaoProduto
    extra = 1
    autocomplete_fields = []

# ADICIONE ESTA NOVA CLASSE
class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1 # Mostra 1 campo extra para adicionar nova imagem

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_base', 'disponivel')
    list_filter = ('disponivel',)
    search_fields = ('nome', 'descricao')
    
    # ADICIONE A NOVA CLASSE INLINE AQUI
    inlines = [
        VariacaoProdutoInline,
        ImagemProdutoInline, # <--- ADICIONE ESTA LINHA
    ]