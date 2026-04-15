import pytest
from main import Produto, ConjuntoDeItens, Cliente, Pedido 

def test_calculo_total_composite():
    """Testa se o Composite soma corretamente produtos e custos extras"""
    p1 = Produto("Pizza", 50.0)
    p2 = Produto("Borda Recheada", 10.0)
    
    combo = ConjuntoDeItens("Combo")
    combo.adicionar(p1).adicionar(p2)
    combo.definir_custo_extra(5.0) # Taxa de serviço
    
    assert combo.obter_preco() == 65.0

def test_fluxo_pedido_completo():
    """Testa se o pedido armazena o total do Composite corretamente"""
    item = Produto("Hambúrguer", 30.0)
    cliente = Cliente("João", "joao@email.com", "123", "123")
    pedido = Pedido(cliente, item)
    
    assert pedido.obter_total() == 30.0
    assert pedido.status == "ABERTO"
