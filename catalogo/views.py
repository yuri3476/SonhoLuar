# catalogo/views.py
import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Produto, VariacaoProduto, Categoria
from django.contrib import messages

def lista_produtos(request):
    """Mostra produtos, filtrando por categoria se solicitado."""
    categoria_slug = request.GET.get('categoria')
    
    produtos = Produto.objects.filter(disponivel=True)
    categoria_atual = None

    if categoria_slug:
        categoria_atual = get_object_or_404(Categoria, slug=categoria_slug)
        produtos = produtos.filter(categoria=categoria_atual)

    categorias = Categoria.objects.all()

    context = {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_atual': categoria_atual,
    }
    return render(request, 'catalogo/lista_produtos.html', context)

def detalhe_produto(request, pk):
    """Mostra a página de um produto específico."""
    produto = get_object_or_404(Produto, pk=pk, disponivel=True)
    context = {
        'produto': produto
    }
    return render(request, 'catalogo/detalhe_produto.html', context)

# catalogo/views.py

def adicionar_ao_carrinho(request, variacao_id):
    """Adiciona item com quantidade e observação."""
    variacao = get_object_or_404(VariacaoProduto, id=variacao_id)
    carrinho = request.session.get('carrinho', {})
    str_variacao_id = str(variacao_id)

    # Pega dados do formulário (POST) ou usa padrão
    quantidade_escolhida = int(request.POST.get('quantidade', 1))
    observacao_cliente = request.POST.get('observacao', '')

    if str_variacao_id in carrinho:
        # Soma a quantidade nova à existente
        carrinho[str_variacao_id]['quantidade'] += quantidade_escolhida
        
        # Se tiver observação nova, sobrescreve/adiciona (opcional: concatenar)
        if observacao_cliente:
            carrinho[str_variacao_id]['observacao'] = observacao_cliente
    else:
        # Novo item
        carrinho[str_variacao_id] = {
            'quantidade': quantidade_escolhida,
            'produto_nome': variacao.produto.nome,
            'tamanho': variacao.tamanho,
            'preco_final': float(variacao.preco_final),
            'observacao': observacao_cliente, # Salva a observação
            'cor_nome': variacao.cor, # Útil para exibir no carrinho
        }

    request.session['carrinho'] = carrinho
    messages.success(request, f"{variacao.produto.nome} adicionado ao carrinho!")
    return redirect('detalhe_produto', pk=variacao.produto.pk)

def ver_carrinho(request):
    """Mostra o carrinho de compras."""
    carrinho = request.session.get('carrinho', {})
    
    itens_carrinho = []
    total_pedido = 0

    # =============================================================
    # MUDANÇA AQUI:
    # Antes: for item in carrinho.values():
    # Precisamos da CHAVE (variacao_id) e do VALOR (item_data)
    # =============================================================
    for variacao_id, item_data in carrinho.items():
        # Adicionamos o ID ao dicionário para o template usá-lo
        item_data['variacao_id'] = variacao_id 
        
        subtotal_item = item_data['quantidade'] * item_data['preco_final']
        item_data['subtotal'] = subtotal_item
        
        itens_carrinho.append(item_data)
        total_pedido += subtotal_item

    context = {
        'itens_carrinho': itens_carrinho,
        'total_pedido': total_pedido,
    }
    return render(request, 'catalogo/carrinho.html', context)

def remover_do_carrinho(request, variacao_id):
    """Remove um item específico do carrinho."""
    carrinho = request.session.get('carrinho', {})
    
    # O variacao_id vindo da URL já é uma string (definido no urls.py)
    if variacao_id in carrinho:
        # Pega o nome para a mensagem antes de deletar
        item_nome = carrinho[variacao_id].get('produto_nome', 'Item')
        
        # Remove o item do dicionário
        del carrinho[variacao_id]
        
        # Salva a sessão atualizada
        request.session['carrinho'] = carrinho
        
        messages.success(request, f"{item_nome} foi removido do carrinho.")
    else:
        messages.error(request, "Item não encontrado no carrinho.")

    # Redireciona de volta para a página do carrinho
    return redirect('ver_carrinho')

# catalogo/views.py

def checkout_whatsapp(request):
    """Formata a mensagem e redireciona para o WhatsApp."""
    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        return redirect('lista_produtos')

    # Configurações
    NUMERO_WHATSAPP = settings.NUMERO_WHATSAPP # Pega do settings.py
    
    mensagem_pedido = ["Olá! 👋 Gostaria de fazer o seguinte pedido:"]
    total_pedido = 0

    for item in carrinho.values():
        subtotal = item['quantidade'] * item['preco_final']
        
        # Monta o bloco de texto básico do item
        # Adicionei a COR aqui também para o pedido ficar completo
        texto_item = (
            f"\n------------------------------\n"
            f"*Produto:* {item['produto_nome']}\n"
            f"*Tamanho:* {item['tamanho']}\n"
            f"*Cor:* {item.get('cor_nome', 'Única')}\n" 
            f"*Qtd:* {item['quantidade']}\n"
            f"*Subtotal:* R$ {subtotal:.2f}"
        )
        
        # --- LÓGICA DA OBSERVAÇÃO ---
        # Verifica se existe observação E se ela não está vazia
        observacao = item.get('observacao', '').strip()
        if observacao:
            texto_item += f"\n*Obs:* _{observacao}_"
        # ----------------------------

        mensagem_pedido.append(texto_item)
        total_pedido += subtotal

    mensagem_pedido.append(f"\n------------------------------\n*Total do Pedido: R$ {total_pedido:.2f}*")
    
    # Limpa o carrinho (opcional: você pode querer limpar só depois de confirmar, mas o padrão é limpar ao gerar o link)
    # request.session['carrinho'] = {} 
    # DICA: Muitos preferem NÃO limpar o carrinho aqui caso o cliente desista no meio do caminho e volte pro site.
    # Se quiser limpar, descomente a linha acima.

    # Formata a mensagem para a URL
    texto_formatado = urllib.parse.quote('\n'.join(mensagem_pedido))
    
    # Cria o link do WhatsApp
    link_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP}?text={texto_formatado}"
    
    return redirect(link_whatsapp)