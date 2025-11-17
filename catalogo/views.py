# catalogo/views.py
import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Produto, VariacaoProduto
from django.contrib import messages

def lista_produtos(request):
    """Mostra a página inicial com todos os produtos disponíveis."""
    produtos = Produto.objects.filter(disponivel=True)
    context = {
        'produtos': produtos
    }
    return render(request, 'catalogo/lista_produtos.html', context)

def detalhe_produto(request, pk):
    """Mostra a página de um produto específico."""
    produto = get_object_or_404(Produto, pk=pk, disponivel=True)
    context = {
        'produto': produto
    }
    return render(request, 'catalogo/detalhe_produto.html', context)

def adicionar_ao_carrinho(request, variacao_id):
    """Adiciona um item ao carrinho na sessão."""
    variacao = get_object_or_404(VariacaoProduto, id=variacao_id)
    
    # ... (toda a sua lógica de adicionar ao carrinho continua igual) ...
    carrinho = request.session.get('carrinho', {})
    str_variacao_id = str(variacao_id)
    if str_variacao_id in carrinho:
        carrinho[str_variacao_id]['quantidade'] += 1
    else:
        if variacao.quantidade_estoque > 0:
            carrinho[str_variacao_id] = {
                'quantidade': 1,
                'produto_nome': variacao.produto.nome,
                'tamanho': variacao.tamanho,
                'preco_final': float(variacao.preco_final),
            }
    request.session['carrinho'] = carrinho
    
    # =============================================================
    # 2. ADICIONE A MENSAGEM DE SUCESSO AQUI
    # =============================================================
    messages.success(request, f"{variacao.produto.nome} (Tam: {variacao.tamanho}) foi adicionado ao carrinho!")

    # O redirect continua o mesmo, voltando para a página do produto
    return redirect('detalhe_produto', pk=variacao.produto.pk)

def ver_carrinho(request):
    """Mostra o carrinho de compras."""
    carrinho = request.session.get('carrinho', {})
    
    itens_carrinho = []
    total_pedido = 0

    for item in carrinho.values():
        subtotal_item = item['quantidade'] * item['preco_final']
        item['subtotal'] = subtotal_item
        itens_carrinho.append(item)
        total_pedido += subtotal_item

    context = {
        'itens_carrinho': itens_carrinho,
        'total_pedido': total_pedido,
    }
    return render(request, 'catalogo/carrinho.html', context)

def checkout_whatsapp(request):
    """Formata a mensagem e redireciona para o WhatsApp."""
    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        return redirect('lista_produtos')

    mensagem_pedido = ["Olá! 👋 Gostaria de fazer o seguinte pedido:"]
    total_pedido = 0

    for item in carrinho.values():
        subtotal = item['quantidade'] * item['preco_final']
        mensagem_pedido.append(
            f"\n*Produto:* {item['produto_nome']}\n"
            f"*Tamanho:* {item['tamanho']}\n"
            f"*Qtd:* {item['quantidade']}\n"
            f"*Subtotal:* R$ {subtotal:.2f}"
        )
        total_pedido += subtotal

    mensagem_pedido.append(f"\n\n*Total do Pedido: R$ {total_pedido:.2f}*")
    
    # Limpa o carrinho
    request.session['carrinho'] = {}

    # Formata a mensagem para a URL
    texto_formatado = urllib.parse.quote('\n'.join(mensagem_pedido))
    
    # Cria o link do WhatsApp
    link_whatsapp = f"https://wa.me/{settings.NUMERO_WHATSAPP}?text={texto_formatado}"
    
    return redirect(link_whatsapp)