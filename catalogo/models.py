# catalogo/models.py
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco_base = models.DecimalField(max_digits=10, decimal_places=2)
    disponivel = models.BooleanField(default=True)
    imagem_principal = models.ImageField(upload_to='produtos/')

    def __str__(self):
        return self.nome

class VariacaoProduto(models.Model):
    produto = models.ForeignKey(Produto, related_name='variacoes', on_delete=models.CASCADE)
    tamanho = models.CharField(max_length=50) # Ex: "P", "M", "G", "40"
    preco_override = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Se vazio, usa o preço base do produto."
    )
    quantidade_estoque = models.PositiveIntegerField(default=0)

    class Meta:
        # Garante que não haja P e P para o mesmo produto
        unique_together = ('produto', 'tamanho')

    def __str__(self):
        return f"{self.produto.nome} - Tam: {self.tamanho} ({self.quantidade_estoque} em estoque)"

    @property
    def preco_final(self):
        return self.preco_override or self.produto.preco_base
     
class ImagemProduto(models.Model):
    produto = models.ForeignKey(Produto, 
                                related_name='imagens_adicionais', 
                                on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/adicionais/')

    class Meta:
        verbose_name = 'Imagem do Produto'
        verbose_name_plural = 'Imagens do Produto'

    def __str__(self):
        return f"Imagem para {self.produto.nome}"