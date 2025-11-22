# catalogo/admin.py
from django.contrib import admin
from .models import Categoria, Produto, VariacaoProduto, ImagemProduto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'ordem')
    prepopulated_fields = {'slug': ('nome',)} # Preenche o slug automaticamente ao digitar o nome

# catalogo/admin.py

class VariacaoProdutoInline(admin.TabularInline):
    model = VariacaoProduto
    extra = 1
    # ADICIONE 'codigo_hex' NESTA LISTA ABAIXO:
    fields = ['tamanho', 'cor', 'codigo_hex', 'quantidade_estoque']

class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_base', 'preco_antigo', 'disponivel')
    list_filter = ('categoria', 'disponivel')
    search_fields = ('nome',)
    inlines = [VariacaoProdutoInline, ImagemProdutoInline]