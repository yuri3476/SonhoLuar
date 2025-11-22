# catalogo/models.py
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="Identificador único para URL (ex: pijamas)")
    ordem = models.IntegerField(default=0, help_text="Ordem de exibição no menu")

    class Meta:
        ordering = ['ordem', 'nome']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='produtos', on_delete=models.SET_NULL, null=True, blank=True)
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    
    # Preço atual (o valor real de venda)
    preco_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Atual")
    
    # Preço antigo (para fazer o efeito de "De R$ 100 por R$ 80")
    preco_antigo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço Antigo (Riscado)")
    
    disponivel = models.BooleanField(default=True)
    imagem_principal = models.ImageField(upload_to='produtos/')

    def __str__(self):
        return self.nome

# catalogo/models.py

class VariacaoProduto(models.Model):
    produto = models.ForeignKey(Produto, related_name='variacoes', on_delete=models.CASCADE)
    tamanho = models.CharField(max_length=50)
    cor = models.CharField(max_length=50, default="Única")
    
    # --- NOVO CAMPO ---
    codigo_hex = models.CharField(max_length=7, default="#ffffff", help_text="Cor em Hex (ex: #000000 para preto)")
    # ------------------
    
    preco_override = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Se vazio, usa o preço base do produto."
    )
    quantidade_estoque = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('produto', 'tamanho', 'cor')

    def __str__(self):
        return f"{self.produto.nome} - {self.tamanho} / {self.cor}"

    @property
    def preco_final(self):
        return self.preco_override or self.produto.preco_base

class ImagemProduto(models.Model):
    produto = models.ForeignKey(Produto, related_name='imagens_adicionais', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/adicionais/')