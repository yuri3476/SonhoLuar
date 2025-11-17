# catalogo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Página inicial
    path('', views.lista_produtos, name='lista_produtos'), 

    # Página de detalhe do produto
    path('produto/<int:pk>/', views.detalhe_produto, name='detalhe_produto'),

    # Ações do Carrinho
    path('add/<int:variacao_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('checkout/', views.checkout_whatsapp, name='checkout_whatsapp'),
]