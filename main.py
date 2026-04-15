from abc import ABC, abstractmethod
from typing import List

# ===================== COMPOSITE =====================

class ItemDePedido(ABC):
    @abstractmethod
    def obter_preco(self) -> float:
        pass
 
    @abstractmethod
    def obter_nome(self) -> str:
        pass
 
class Produto(ItemDePedido):
    def __init__(self, nome: str, preco: float):
        self._nome = nome
        self._preco = preco
 
    def obter_preco(self) -> float:
        return self._preco
 
    def obter_nome(self) -> str:
        return self._nome
 
class ConjuntoDeItens(ItemDePedido):
    def __init__(self, nome: str):
        self._nome = nome
        self._itens_internos: List[ItemDePedido] = []
        self._custo_extra_do_conjunto = 0.0
 
    def adicionar(self, item: ItemDePedido):
        self._itens_internos.append(item)
        return self
 
    def definir_custo_extra(self, valor: float):
        self._custo_extra_do_conjunto = valor
        return self
 
    def obter_preco(self) -> float:
        subtotal = sum(item.obter_preco() for item in self._itens_internos)
        return subtotal + self._custo_extra_do_conjunto
 
    def obter_nome(self) -> str:
        return self._nome
 
    def descrever_arvore(self, nivel: int) -> str:
        espacos = " " * nivel
        resultado = f"{espacos}- {self._nome} (Conjunto) → R$ {self.obter_preco():.2f}\n"
 
        for item in self._itens_internos:
            if isinstance(item, ConjuntoDeItens):
                resultado += item.descrever_arvore(nivel + 2)
            else:
                espacos_item = " " * (nivel + 2)
                resultado += f"{espacos_item}• {item.obter_nome()} (Produto) → R$ {item.obter_preco():.2f}\n"
 
        if self._custo_extra_do_conjunto > 0:
            espacos_extra = " " * (nivel + 2)
            resultado += f"{espacos_extra}(Custo extra do conjunto: R$ {self._custo_extra_do_conjunto:.2f})\n"
 
        return resultado
 
# ===================== CLIENTE =====================

class Cliente:
    def __init__(self, nome: str, email: str, sms: str, whatsapp: str):
        self.nome = nome
        self.email = email
        self.sms = sms
        self.whatsapp = whatsapp
 
# ===================== DECORATOR =====================

class Notificador(ABC):
    @abstractmethod
    def enviar(self, mensagem: str, destinatario: Cliente):
        pass
 
class NotificadorEmail(Notificador):
    def enviar(self, mensagem: str, destinatario: Cliente):
        if destinatario.email:
            print(f"[Email] Para {destinatario.email}: {mensagem}")
 
class DecoradorDeNotificacao(Notificador):
    """Classe base para decoradores que envolvem um Notificador."""
    def __init__(self, notificador_interno: Notificador):
        self._notificador_interno = notificador_interno
 
    def enviar(self, mensagem: str, destinatario: Cliente):
        # Repassa a chamada para o próximo notificador na pilha
        self._notificador_interno.enviar(mensagem, destinatario)
 
class NotificadorSMS(DecoradorDeNotificacao):
    def enviar(self, mensagem: str, destinatario: Cliente):
        super().enviar(mensagem, destinatario)
        if destinatario.sms:
            print(f"[SMS] Para {destinatario.sms}: {mensagem}")
 
class NotificadorWhatsApp(DecoradorDeNotificacao):
    def enviar(self, mensagem: str, destinatario: Cliente):
        super().enviar(mensagem, destinatario)
        if destinatario.whatsapp:
            print(f"[WhatsApp] Para {destinatario.whatsapp}: {mensagem}")
 
# ===================== PEDIDO =====================

class Pedido:
    def __init__(self, cliente: Cliente, raiz_dos_itens: ItemDePedido):
        self.cliente = cliente
        self.raiz_dos_itens = raiz_dos_itens
        self.status = "ABERTO"
 
    def obter_total(self) -> float:
        return self.raiz_dos_itens.obter_preco()
 
    def gerar_resumo_texto(self) -> str:
        if isinstance(self.raiz_dos_itens, ConjuntoDeItens):
            resumo_itens = self.raiz_dos_itens.descrever_arvore(2)
        else:
            resumo_itens = f"  • {self.raiz_dos_itens.obter_nome()} → R$ {self.raiz_dos_itens.obter_preco():.2f}\n"

        return (f"Cliente: {self.cliente.nome}\n"
                f"Itens:\n{resumo_itens}"
                f"Total: R$ {self.obter_total():.2f}")
 
    def realizar_checkout(self, notificador: Notificador) -> str:
        if self.status != "ABERTO":
            raise ValueError("Pedido já finalizado.")

        self.status = "PAGO"
        mensagem = f"Seu pedido foi confirmado! Total: R$ {self.obter_total():.2f}"
        notificador.enviar(mensagem, self.cliente)
        return mensagem
 
# ===================== MAIN =====================

if __name__ == "__main__":
    # Montando a árvore de itens
    pedido_raiz = ConjuntoDeItens("Pedido #PZ-2025-0004")
 
    combo_festa = ConjuntoDeItens("Combo Festa")
    bebidas = ConjuntoDeItens("Bebidas")
 
    pizza_gigante = ConjuntoDeItens("Pizza Gigante 3 Sabores").definir_custo_extra(7.50)
    pizza_media = ConjuntoDeItens("Pizza Média Tradicional")
 
    pizza_gigante.adicionar(Produto("1/3 Calabresa", 35.90))\
                 .adicionar(Produto("1/3 Frango com Catupiry", 36.90))\
                 .adicionar(Produto("1/3 Quatro Queijos", 34.90))\
                 .adicionar(Produto("Adicional Bacon", 5.90))
 
    pizza_media.adicionar(Produto("Base Mussarela", 29.90))\
               .adicionar(Produto("Adicional Tomate Seco", 3.50))
 
    bebidas.adicionar(Produto("Refrigerante 2L", 10.90))\
           .adicionar(Produto("Suco de Uva 500ml", 6.90))
 
    combo_festa.adicionar(pizza_gigante).adicionar(pizza_media)
 
    pedido_raiz.adicionar(combo_festa)\
               .adicionar(bebidas)\
               .definir_custo_extra(4.00) # Taxa de entrega/embalagem
 
    cliente_exemplo = Cliente("Maria PizzaLover", "maria.pizza@example.com", 
                             "+55 11 91234-5678", "+55 11 91234-5678")

    pedido = Pedido(cliente_exemplo, pedido_raiz)
 
    print("===== RESUMO DO PEDIDO =====")
    print(pedido.gerar_resumo_texto())
 
    # Configurando os Decorators (Pilha: Email -> SMS -> WhatsApp)
    notificador = NotificadorEmail()
    notificador = NotificadorSMS(notificador)
    notificador = NotificadorWhatsApp(notificador)
 
    print("\n===== CONFIRMAÇÃO DE PEDIDO =====")
    pedido.realizar_checkout(notificador)
